(($) => {
    console.log(voting);
    app.getVotingCount().then(data => {
        console.log(data);

        
    });
    setInterval(() => {
        console.log(`Refrescando resultados de la votación: ${voting.id}`);
        //app.getVotingCount();
    }, 1000);
})(jQuery);