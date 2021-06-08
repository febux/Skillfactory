let arr = [1, 2 ,4, 6, 7, 8];
let is_similar = false;

for (i = 0; i < arr.length; i++) {
    for (j = 0; j < arr.length; j++) {
        if (i === j){
            break;
        }
        if (arr[i] === arr[j]) {
            is_similar = true;
        }
    }
}
console.log(is_similar);