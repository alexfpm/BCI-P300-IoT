/*Developed by: Joel Murphy and Conor Russomanno (Summer 2013)
 * Modified by: Alex PM (2022)
 * 
 * 
  This example uses the ADS1299 Arduino Library, a software bridge between the ADS1299 TI chip and 
  Arduino. See http://www.ti.com/product/ads1299 for more information about the device and the README
  folder in the ADS1299 directory for more information about the library.
  
  This program does the following
  It reads in all registers in verbose mode, then alters the CONFIG3 register,
  then asks for a prompt to take numSampGG samples at the default rate of 250sps.
  
  At the prompt, the START command is sent, and a mS timestamp is saved (optional).
  A function called ADStest() proceeds to poll the DRDY pin, and call
  the updateChanelData() member funcion until all samples are counted.
  Then another timestamp is taken, duration of event is calculated and 
  printed to terminal. Then the prompt re-appears.
  The library outputs verbose feedback when verbose is true.
  
  Arduino Uno - Pin Assignments
  SCK = 13
  MISO [DOUT] = 12
  MOSI [DIN] = 11
  CS = 10; 
  RESET = 9;
  DRDY = 8;
  
*/

#include "ADS1299.h"

ADS1299 ADS;                           // create an instance of ADS1299

unsigned long thisTime;                
unsigned long thatTime;
unsigned long elapsedTime;
int resetPin = 9;                      // pin 9 used to start conversion in Read Data Continuous mode
int sampleCounter = 0;                 // used to time the tesing loop
boolean testing = false;               // this flag is set in serialEvent on reciept of prompt



// Cont for loops, and definition for number of samples
int contSamp;

//int numSampGG = 250/9;
//int numSampGG = 28;   // 250/9 es aproximado a 28
//int numSampGG = 250/20; //Para el Real-Time Mode de Matplotlib (SIN KIVY)
int numSampGG = 250/20;



void setup() {
  // don't put anything before the initialization routine for recommended POR  
  ADS.initialize(8,9,10,4,false); // (DRDY pin, RST pin, CS pin, SCK frequency in MHz);

  Serial.begin(230400);
  Serial.println("ADS1299-Arduino UNO Example 2");
  Serial.println("--------------------------------------------------------"); 
  delay(2000);             

  ADS.verbose = true;      // when verbose is true, there will be Serial feedback 
  ADS.RESET();             // send RESET command to default all registers
  ADS.SDATAC();            // exit Read Data Continuous mode to communicate with ADS
  ADS.RREGS(0x00,0x17);     // read all registers starting at ID and ending at CONFIG4
  
  Serial.println("--------------------------------------------------------");
  ADS.WREG(CONFIG3,0xE0);  // enable internal reference buffer, for fun
  ADS.RREG(CONFIG3);       // verify write
  Serial.println("--------------------------------------------------------");

  ADS.WREG(CONFIG2,0xC0);   //C0 es para leer de los canales
  ADS.RREG(CONFIG2);
  Serial.println("--------------------------------------------------------");

  //Modify registers of Channels
  
  for(byte i = CH1SET; i <= CH8SET; i++){  //setup to modify the 8 channels setting registers
    ADS.regData[i] = 0x60;                 //0x60 para leer de los canales
  }
  

  ADS.WREGS(CH1SET,7);               // write new channel settings
  ADS.RREGS(CH1SET,7);               // read out what we just did to verify the write
  
  Serial.println("--------------------------------------------------------");

  //-------------------------------------------------------------------------------------------------------------
  Serial.println("--------------------------------------------------------");
  
  ADS.WREG(MISC1,0x20);  // change register
  ADS.RREG(MISC1);       // verify write
  
  ADS.WREG(GPIO,0x00);  // change register
  ADS.RREG(GPIO);       // verify write

  ADS.WREG(CONFIG1,0x96);  // inside CONFIG1 is the sample rate: this commands change the SPS
  ADS.RREG(CONFIG1);       // verify write
  Serial.println("--------------------------------------------------------");

    
  //-------------------------------------------------------------------------------------------------------------
  
  ADS.RDATAC();            // enter Read Data Continuous mode
  
  Serial.println("Press 'x' to begin test");    // ask for prompt
} // end of setup

void loop(){
  
  if (testing){

    //------------------------------------------------------------------------
    //MEASUREMENTS
    //------------------------------------------------------------------------
    
    elapsedTime = 0;


    ADS.START();                    // start sampling
    //thatTime = millis();            // timestamp

    //NUMBER OF SAMPLES FOR THE TEST
    //ADStest(500);                   // go to testing routine and specify the number of samples to take
    ADStest(numSampGG);
    
    
    //thisTime = millis();            // timestamp
    ADS.STOP();                     // stop the sampling
    
    //elapsedTime = elapsedTime + thisTime - thatTime;

    
    sampleCounter = 0;              // reset counter
    //delay(50);

    

    //Printint data just for benchmark (Optional)
    //Serial.print("Elapsed Time ");Serial.println(elapsedTime);  // benchmark
    //Serial.print("Samples ");Serial.println(numSampGG*numCycles);   // 
    //sampleCounter = 0;              // reset counter
    

  }// end of testing
  
} // end of loop



//SENDING AN "x" STARTS READING. AND, SENDING AN "z" STOPS THE READING

void serialEvent(){            // send an 'x' on the serial line to trigger ADStest()
  while(Serial.available()){      
    char inChar = (char)Serial.read();
    
    if (inChar  == 'x'){

      //delay(5000);
      delay(1000);
      
      testing = true;
    }

    if (inChar  == 'z'){   
      testing = false;
      
      Serial.println("\n MENU: \n");  // ask for prompt
      Serial.println("-Press 'x' to start sampling \n");
      Serial.println("-Press 'z' to stop sampling");
    }
  }
}

void ADStest(int numSamples){
  while(sampleCounter < numSamples){  // take only as many samples as you need
    while(digitalRead(8)){            // watch the DRDY pin
      }
    ADS.updateChannelData();          // update the channelData array 
    sampleCounter++;                  // increment sample counter for next time
  }
    return;
}
