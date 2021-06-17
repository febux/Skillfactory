function searching_simple_number(num){

    if (num>=1000){
        console.log(`Your number ${num} is impermissible.`);
    }
    if (num<1000){
        if (num===0 || num===1){
            return console.log(`Your number ${num} is not simple.`);
        }

        for(i=2;i<=Math.sqrt(num);i++){
            if (num%i===0) {
                return console.log(`Your number ${num} is not simple.`);
            }

        }
        return console.log(`Your number ${num} is simple.`);
    }
}

searching_simple_number(12)