function func(num1){
    return func1(num2)
}

function func1(num2){
    return num1+num2;
}

result = func(num1=5, num2=6)

console.log(`My function is ${result}.`);