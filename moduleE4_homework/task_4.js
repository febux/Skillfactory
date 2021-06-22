function Appliance(name, current, usage){
    this.name = name
    this.usage = usage
    this.voltage = 220
    this.current = current
    this.switch = false
}

Appliance.prototype.getUsage = function(){
    console.log(`Usage of ${this.name} is ${this.usage}`);
}

Appliance.prototype.switchOn = function(){
    if (this.switch === false){
        this.switch = true;
    }
    console.log(`${this.name} is switched ON`);
}

Appliance.prototype.switchOff = function(){
    if (this.switch === true){
        this.switch = false;
    }
    console.log(`${this.name} is switched OFF`);
}

Appliance.prototype.getConsumption = function(){
    if (this.switch === true){
        let consumption = this.voltage * this.current;
        console.log(`Сonsumption of ${this.name} is ${consumption} W`);
    }
    else{
        console.log(`Сonsumption of ${this.name} is 0 W`);
    }

}

function ElectronicalAppliance(name, voltage, current, usage){
    this.name = name
    this.usage = usage
    this.voltage = voltage
    this.current = current
    this.switch = false
    this.sleepMode = function (turn){
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

ElectronicalAppliance.prototype = new Appliance();

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
personalComputer.sleepMode(true);
personalComputer.getConsumption();

// console.log(tableLamp);
// console.log(personalComputer);