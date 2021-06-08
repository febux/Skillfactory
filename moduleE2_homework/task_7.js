let arr = [1, 2 ,4, 6, 7, 8];
let odd_number = 0;
let even_number = 0;

for (i = 0; i < arr.length; i++) {
    if (arr[i]%2 === 0){
        even_number += 1;
    }
    else {
        odd_number += 1;
    }
}
console.log(`The amount of even numbers is ${even_number}`);
console.log(`The amount of odd numbers is ${odd_number}`);