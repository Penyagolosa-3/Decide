(($) => {
    class VotingCount {
        constructor(options) {
            this.options = options;
        }
        putOptionsValues(votingCountFetch) {
            let categorizedVoting = this.categorizeVotingCount(votingCountFetch);
            for(let v of categorizedVoting) {
                let option_id = v.option_id,
                    found = false;
                for(let o of this.options) {
                    if(o.number==option_id) {
                        o.votingCount = v.count;
                        found = true;
                    }
                }
            }
            console.log(this.options);
            app.setOptions(this.options);
            app.$forceUpdate();
        }
        categorizeVotingCount(votingCount) {
            let categorized = [];
            for(let v of votingCount) {
                let option_id = v.option_id,
                    found = false;

                for(let i=0; i<categorized.length&&!found; i++) {
                    let c = categorized[i];

                    if(c.option_id==option_id) {
                        found = true;
                        c.value++;
                    }
                }
                if(!found) {
                    categorized.push({
                        ...v,
                        ...{
                            count: 1
                        }
                    });
                }
            }
            return categorized;
        }
    }

    let votingCount = new VotingCount(voting.question.options);

    setInterval(() => {
        console.log(`Refrescando resultados de la votación: ${voting.id}`);

        app.getVotingCount().then(data => {
            console.log(data);
            votingCount.putOptionsValues(data);
        });
    }, 1000);
})(jQuery);