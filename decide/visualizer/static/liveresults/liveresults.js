(($) => {
    console.log(voting);
    app.getVotingCount();
    setInterval(() => {
        console.log(`Refrescando resultados de la votación: ${voting.id}`);
        //app.getVotingCount();
    }, 1000);
})(jQuery);