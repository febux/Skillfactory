let map = new Map([
    ["apple", "green"],
    ["strawberry", "red"],
    ["blueberry",    "blue"],
    [true, "boolean"],
    [1, "number"],
    ["hello", "string"],
]);

for (let elem of map) {
    console.log(`The key is ${elem[0]}, The value is ${elem[1]}`);
}