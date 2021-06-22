const user = {

    name: 'Andrei',

    surname: 'Ivanov',

    age: 18,

    position: 'developer',

};

let string = 'age'

function compare_string_and_obj(str, obj){
    return str in obj;
}

console.log(compare_string_and_obj(string, user))