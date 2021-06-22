class Appliance{
    constructor(name, current, usage){
        this.name = name
        this.usage = usage
        this.voltage = 220
        this.current = current
        this.switch = false
    }
    getUsage(){
        console.log(`Usage of ${this.name} is ${this.usage}`);
    }
    switchOn(){
        if (this.switch === false){
            this.switch = true;
        }
        console.log(`${this.name} is switched ON`);
    }
    switchOff(){
        if (this.switch === true){
            this.switch = false;
        }
        console.log(`${this.name} is switched OFF`);
    }
    getConsumption(){
        if (this.switch === true){
            let consumption = this.voltage * this.current;
            console.log(`Сonsumption of ${this.name} is ${consumption} W`);
        }
        else{
            console.log(`Сonsumption of ${this.name} is 0 W`);
        }

    }

}

class ElectronicalAppliance extends Appliance {
    constructor(name, voltage, current, usage) {
        super(name, current, usage);
        this.voltage = voltage
    }
    sleepMode(turn){
        if (this.switch === true){
            if (turn === true){
                this.current = this.current / 100;
            }
            else{
                this.current = this.current * 100;
            }
        }
        else{
            console.log(`${this.name} is switched OFF`);
        }

    }
}

const tableLamp = new Appliance('Lamp',1, 'light');
const personalComputer = new ElectronicalAppliance('PC', 230, 3.5, 'calculate');
console.log(tableLamp);
console.log(personalComputer);


tableLamp.getUsage();
personalComputer.getUsage();
personalComputer.getConsumption();
tableLamp.getConsumption();
personalComputer.switchOn();
personalComputer.getConsumption();
tableLamp.getConsumption();
personalComputer.switchOff();
personalComputer.getConsumption();
tableLamp.getConsumption();

personalComputer.sleepMode(true);
personalComputer.getConsumption();
personalComputer.switchOn();
tableLamp.switchOn();
personalComputer.sleepMode(true);
personalComputer.getConsumption();
tableLamp.getConsumption();

// console.log(tableLamp);
// console.log(personalComputer);