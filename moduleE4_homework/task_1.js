const user = {

    name: 'Andrei',

    surname: 'Ivanov',

    age: 18,

    position: 'developer',

};

function return_keys_and_values (obj){
    for (let key in obj) {

        console.log(key);
        console.log(obj[key]);
    }
}

return_keys_and_values(user)