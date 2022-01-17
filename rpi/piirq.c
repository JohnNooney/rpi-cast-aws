/*
 ============================================================================
 Name        : piirq02.c
 Author      : John Nooney
 Version     : 0.1
 Copyright   : See Abertay copyright notice
 Description : RPi Zero Wireless - IRQ with LED and Push button for RPiPlay status updates
 ============================================================================
 */
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/interrupt.h>
#include <linux/stdlib.h>

//Red LED = BCM pin 18
//Green LED = BCM pin 24
//button = BCM pin 3

static bool	State = 0;
static unsigned int Led = 23;
static unsigned int Button = 3;
static unsigned int Irqnum = 0;
static unsigned int Counter = 0;

static irq_handler_t piirq_irq_handler(unsigned int irq, void *dev_id, struct pt_regs *regs){
   State = !State;
   gpio_set_value(Led, State);

   printk(KERN_INFO "piirq: led state is : [%d] ", gpio_get_value(Led));
   printk(KERN_INFO "piirq: button state is : [%d] ", gpio_get_value(Button));

   Counter++;
   return (irq_handler_t) IRQ_HANDLED;
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

	   gpio_request(Led, "Led");
	   gpio_direction_output(Led, 1);
	   // Causes to appear in /sys/class/gpio/gpio16 for echo 0 > value
	   gpio_export(Led, false);
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
MODULE_AUTHOR("Nooney CMP408");
MODULE_DESCRIPTION("RPi IRQ Test with 2 lights");
MODULE_VERSION("0.5");
