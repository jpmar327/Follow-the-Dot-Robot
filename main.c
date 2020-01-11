// Get Coordinates of pieces via UART
// tell motor to spin to make appropriate changes

#include "msp.h"
#include "driverlib.h"
#include "stdio.h"

uint32_t SMCLK_divider = CS_CLOCK_DIVIDER_1 ;
#define timerA_divider   TIMER_A_CLOCKSOURCE_DIVIDER_64   // Means counter is incremented at 1E+6/64 = 15625 Hz
#define timerA_period    15625

const eUSCI_UART_Config UART_init =
    {
     EUSCI_A_UART_CLOCKSOURCE_SMCLK,
     3,
     4,
     2,
     EUSCI_A_UART_NO_PARITY,
     EUSCI_A_UART_LSB_FIRST,
     EUSCI_A_UART_ONE_STOP_BIT,
     EUSCI_A_UART_MODE,
     EUSCI_A_UART_OVERSAMPLING_BAUDRATE_GENERATION
    };


volatile int coordinates[6];  //blue  = checker; red  = center; black = magnet   [cx_blue, cy_blue, cx_black, cy_black, cx_red, cy_red]
volatile char num[3];
volatile int coord;
volatile int idxCoord;
volatile int idxNum;
volatile int xOrigin = 625/2;
volatile int yOrigin = 475/2;


void main(void)
{
    printf("x");

    WDT_A_holdTimer();
    int xspeed = 0;    // speed for stepper motor in x direction
    int yspeed = 0;    // speed for stepper motor in y direction
    int mode = 0;
    int error = 60;
    int topSpeed = 7000;
    int i;
    int delayStop = 1500;
    int delayRun = 1000;

    /////////////////////////// Enable Motor /////////////////////////////////
    CS_setDCOFrequency(3E+6); // Set DCO clock source frequency
    CS_initClockSignal(CS_SMCLK , CS_DCOCLK_SELECT, CS_CLOCK_DIVIDER_1); // Tie SMCLK to DCO

    P2SEL0 |= 0x10;    // Set bit 4 of P2SEL0 to enable TA0.1 functionality on P2.4
    P2SEL1 &= ~0x10;   // Clear bit 4 of P2SEL1 to enable TA0.1 functionality on P2.4
    P2DIR |= 0x10;    // Set pin 2.4 as an output pin

    P2SEL0 |= BIT5; // Set bit 5 of P2SEL0 to enable TA0.2 functiosnality on P2.5
    P2SEL1 &= ~BIT5; // Clear bit 4 of P2SEL1 to enable TA0.2 functionality on P2.5
    P2DIR |= BIT5; // Set pin 2.5 as an output pin

    TA0CCR0 = 10000; // Set Timer A period (PWM signal period)
    TA0CCR1 = xspeed; // Set Duty cycle
    TA0CCR2 = yspeed; // Set Duty cycle

    // Set output mode to Reset/Set
    TA0CCTL1 = OUTMOD_7; // Macro which is equal to 0x00e0, defined in msp432p401r.h
    TA0CTL = TASSEL__SMCLK | MC__UP | TACLR;   // Tie Timer A to SMCLK, use Up mode, and clear TA0R

//    Interrupt_enableMaster();
    // PWM signal will now be available on P2.4
    WDT_A_holdTimer();
    GPIO_setAsOutputPin(GPIO_PORT_P1, GPIO_PIN6); // Direction control signal for x stepper motor
    GPIO_setAsOutputPin(GPIO_PORT_P1, GPIO_PIN7); // Direction control for y stepper motor
    ///////////////////////////////////////////////////////////////////////////
    GPIO_setAsInputPinWithPullUpResistor(GPIO_PORT_P1, GPIO_PIN1);


    //////////////////////////// UART Setup ///////////////////////////////////
    UART_initModule(EUSCI_A0_BASE, &UART_init);
    UART_enableModule(EUSCI_A0_BASE);

    // Enable UART receive interrupt
    GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P1, GPIO_PIN2, GPIO_PRIMARY_MODULE_FUNCTION);
    GPIO_setAsPeripheralModuleFunctionOutputPin(GPIO_PORT_P1, GPIO_PIN3, GPIO_PRIMARY_MODULE_FUNCTION);

    UART_enableInterrupt(EUSCI_A0_BASE, EUSCI_A_UART_RECEIVE_INTERRUPT);
    Interrupt_enableInterrupt(INT_EUSCIA0);
    Interrupt_enableMaster();
    ///////////////////////////////////////////////////////////////////////////
    while(1){
//        if (GPIO_INPUT_PIN_LOW == GPIO_getInputPinValue(GPIO_PORT_P1,GPIO_PIN1)) { // Turn Motor on and off
//            TA0CCR1 = 0; // Set Duty cycle
//            TA0CCR2 = 0;
//        }
        if (mode == 0) { // waiting till 3 colors detected
            if ((coordinates[0] != 0 || coordinates[1] != 0) && (coordinates[2] != 0 || coordinates[3] != 0) && (coordinates[4] != 0 || coordinates[5] != 0)) {
                mode = 1;
            }
        } else if (mode == 1) { //moving to checker

            float xToChecker; // x distance from magnet to checker
            float yToChecker; // y distance from magnet to checker

            xToChecker = coordinates[2] - coordinates[0];
            xspeed = abs(xToChecker/625*topSpeed); //  proportional speed control x direction

            yToChecker = coordinates[3] - coordinates[1];
            yspeed = abs(xToChecker/475*topSpeed); //  proportional speed control y direction

            // Control stepper motor
            if(xToChecker > error || xToChecker < -error) { // Checks if x distance is too much
                //printf("x");
                TA0CCR2 = 0; // Turn off y Stepper Motor
                if (xToChecker < -error) {
                    // Enable Stepper motor to move one direction
                    //printf("CCW\n");
                    GPIO_setOutputHighOnPin(GPIO_PORT_P1, GPIO_PIN6); //CCW
                    TA0CCR1 = xspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR1 = 0;
                    for (i=0; i<delayStop; i++){}
                } else if (xToChecker > error) {
                    //printf("CW\n");
                    // Enable Stepper motor to move the other direction
                    GPIO_setOutputLowOnPin(GPIO_PORT_P1, GPIO_PIN6); //CW
                    TA0CCR1 = xspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR1 = 0;
                    for (i=0; i<delayStop; i++){}
                }
            } else if (yToChecker > error || yToChecker < -error) { // Checks if y distance is too much
                TA0CCR1 = 0; // Turn of x Stepper Motor
                //printf("y");

                if (yToChecker > -error) { // Enable y Stepper motor to move one direction
                    GPIO_setOutputHighOnPin(GPIO_PORT_P1, GPIO_PIN7); //CCW
                    TA0CCR2 = yspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR2 = 0;
                    for (i=0; i<delayStop; i++){}
                } else if (yToChecker < error) { // Enable y Stepper motor to move other direction
                    GPIO_setOutputLowOnPin(GPIO_PORT_P1, GPIO_PIN7); //CW
                    TA0CCR2 = yspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR2 = 0;
                    for (i=0; i<delayStop; i++){}
                }
            } else if ((xToChecker < error && xToChecker > -error) && (yToChecker < error && yToChecker > -error)){ // checks if magnet has made it to checker
                mode = 0;
                // Turn off both motors
                TA0CCR1 = 0;
                TA0CCR2 = 0;
                // TODO: Turn on Magnet
            }

        } else if (mode == 2) { //moving checker to center
            float xToCenter; // x distance from magnet to checker
            float yToCenter; // y distance from magnet to checker

            xToCenter = coordinates[0] - coordinates[2];
            xspeed = abs(xToCenter/625*topSpeed); //  proportional speed control x direction

            yToCenter = coordinates[1] - coordinates[3];
            yspeed = abs(xToCenter/475*topSpeed); //  proportional speed control y direction

            // Control stepper motor
            if(xToCenter > error || xToCenter < -error) { // Checks if x distance is too much
                TA0CCR2 = 0; // Turn off y Stepper Motor
                if (xToCenter > error) {
                    // Enable Stepper motor to move x one direction
                    GPIO_setOutputHighOnPin(GPIO_PORT_P1, GPIO_PIN6);
                    TA0CCR1 = xspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR1 = 0;
                    for (i=0; i<delayStop; i++){}
                } else if (xToCenter < -error) {
                    // Enable Stepper motor to move x other direction
                    GPIO_setOutputLowOnPin(GPIO_PORT_P1, GPIO_PIN6);
                    TA0CCR1 = xspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR1 = 0;
                    for (i=0; i<delayStop; i++){}
                }
            } else if (yToCenter > error || yToCenter < -error) { // Checks if y distance is too much
                if (yToCenter > error) {
                    TA0CCR1 = 0; // Turn off x Stepper Motor
                    // Enable Stepper motor to move x one direction
                    GPIO_setOutputHighOnPin(GPIO_PORT_P1, GPIO_PIN7);
                    TA0CCR2 = yspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR2 = 0;
                    for (i=0; i<delayStop; i++){}
                } else if (yToCenter < -error) {
                    // Enable Stepper motor to move x other direction
                    GPIO_setOutputLowOnPin(GPIO_PORT_P1, GPIO_PIN7);
                    TA0CCR2 = yspeed;
                    for (i=0; i<delayRun; i++){}
                    TA0CCR1 = 0;
                    for (i=0; i<delayStop; i++){}
                }
            } else if ((xToCenter < error && xToCenter > -error) && (yToCenter < error && yToCenter > -error)){ // checks if checker has made it to center
                mode = 0;
                // Turn off both motors
                TA0CCR1 = 0;
                TA0CCR2 = 0;
                // TODO: Turn Off Magnet
            }
        }
    }
}

void EUSCIA0_IRQHandler(void) {
    uint8_t cur_char;
    cur_char = UART_receiveData(EUSCI_A0_BASE);


    if (cur_char == 44) {
        coordinates[idxCoord] = atoi(num);
        idxCoord++;
        idxNum = 0;
        num[0] = '\0';
        num[1] = '\0';
        num[2] = '\0';
    } else if (cur_char == 13) {
        coordinates[idxCoord] = atoi(num);
        idxNum = 0;
        idxCoord = 0;
        num[0] = '\0';
        num[1] = '\0';
        num[2] = '\0';
        coordinates[4] = xOrigin;
        coordinates[5] = yOrigin;

    } else {
        num[idxNum] = cur_char;
        idxNum++;
    }
}

