function range(from, to){
    let current = from;
    const intervalId = setInterval(function() {
    console.log(`${current}`);
        if (current == to) {
            clearInterval(intervalId);
        }

    current++;
    }, 1000);

}

range(5, 14)