/*
 ============================================================================
 Name        : piirq02.c
 Author      : John Nooney
 Version     : 0.5
 Copyright   : See Abertay copyright notice
 Description : RPi Zero Wireless - IRQ for gpio button and LED. Will also start subprocess for programs
 ============================================================================
 */
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/interrupt.h>
#include <linux/kmod.h>

static bool	State = 0;
static unsigned int Led = 24;
static unsigned int Led2 = 18;
static unsigned int Button = 3;
static unsigned int Irqnum = 0;
static unsigned int Counter = 0;

//setup env variables to be used in subprocesses
static char *envp[] = {"SHELL=/bin/bash",
            "HOME=/home/pi",
            "USER=pi",
            "TERM=linux",
            "PATH=/sbin:/usr/sbin:/bin:/usr/bin",
            NULL};

//CURRENTLY DOES NOT WORK - subproccess never execute!! 
//See gpicontroller.py for alternate code that works
static irq_handler_t piirq_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){
   State = !State;

    //turn on green light
    gpio_set_value(Led, State);

    //turn on redlight 
    gpio_set_value(Led2, State);

    
    printk(KERN_INFO "piirq: led state is : [%d] ", gpio_get_value(Led));
    printk(KERN_INFO "piirq: button state is : [%d] ", gpio_get_value(Button));

    //start subprocesses
   if(State){

        //Run subprocess in user space to log to AWS
        char *argv[] = {"/bin/sh", "/home/pi/logger.sh", NULL};
        
        //blink LED for visual cue
        gpio_set_value(Led, 0);
        call_usermodehelper(argv[0], argv, envp, UMH_NO_WAIT);
        printk(KERN_INFO "AWS logger.sh subprocess queued");

        //Run subprocess in user space to start AirPlay Server
        char *argv2[] = {"/home/pi/Downloads/RpiPlay/build/rpiplay", NULL};
        call_usermodehelper(argv2[0], argv2, envp, UMH_NO_WAIT);
        printk(KERN_INFO "RPiPlay subprocess queued");
   
   }
   else{
        //run subprocess to shutdown
        char *argv3[] = {"/bin/shutdown", "now", NULL};
        call_usermodehelper(argv3[0], argv3, envp, UMH_NO_WAIT);
        printk(KERN_INFO "Shutting down now subprocess queued");
   }
   
   


   return (irq_handler_t) IRQ_HANDLED;
   Counter++;
}
int __init piirq_init(void){
	int result = 0;
    pr_info("%s\n", __func__);
    //https://www.kernel.org/doc/Documentation/pinctrl.txt
	printk("piirq: IRQ Test");
    printk(KERN_INFO "piirq: Initializing driver\n");

    if (!gpio_is_valid(Led)){
    	printk(KERN_INFO "piirq: invalid GPIO\n");
    return -ENODEV;
   }

    if (!gpio_is_valid(Led2)){
		printk(KERN_INFO "piirq: invalid GPIO LED2\n");
	return -ENODEV;
   }

	   gpio_request(Led, "Led");
	   gpio_direction_output(Led, 1);
	   // Causes to appear in /sys/class/gpio/gpio16 for echo 0 > value
	   gpio_export(Led, false);

	   gpio_request(Led2, "Led2");
	   gpio_direction_output(Led2, 1);
	   // Causes to appear in /sys/class/gpio/gpio16 for echo 0 > value
	   gpio_export(Led2, false);

	   gpio_request(Button, "Button");
	   gpio_direction_input(Button);
	   gpio_set_debounce(Button, 200);
	   gpio_export(Button, false);


    Irqnum = gpio_to_irq(Button);
    printk(KERN_INFO "piirq: The button is mapped to IRQ: %d\n", Irqnum);

    result = request_irq(Irqnum,
		  (irq_handler_t) piirq_irq_handler, // pointer to the IRQ handler
		  IRQF_TRIGGER_RISING,
		  "piirq_handler",    // cat /proc/interrupts to identify
		  NULL);

    printk("piirq loaded\n");
    return 0;
}
void __exit piirq_exit(void){
   gpio_set_value(Led, 0);
   gpio_unexport(Led);
   free_irq(Irqnum, NULL);
   gpio_unexport(Button);
   gpio_free(Led);
   gpio_free(Button);
   printk("piirq unloaded\n");
}
module_init(piirq_init);
module_exit(piirq_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Nooney");
MODULE_DESCRIPTION("RPi AirPlay and AWS LKM");
MODULE_VERSION("0.5");
