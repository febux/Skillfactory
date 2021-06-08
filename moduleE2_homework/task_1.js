t = prompt('enter number:');
t = +t;
if (typeof t  == 'number') {

    console.log(`number ${t}`)
    if (t%2 === 0) {
        console.log('even number')
    }
    else {
        console.log('odd number')
    }
}
else {
    console.log('Oops, you are wrong.')
}
