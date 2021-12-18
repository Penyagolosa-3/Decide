(($) => {
    console.log(voting);

    setInterval(() => {
        console.log(voting.postproc[0].votes);
    }, 1000);

    
})(jQuery);