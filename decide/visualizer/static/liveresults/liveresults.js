(() => {
    class VotingCount {
        constructor(app, options, fetchInterval = 2500) {
            this.totalVotes = 0;
            this.app = app;
            this.fetchInterval = fetchInterval;
            this.options = options;
            this.intervalFetch();
        }

        /*
         * Descripción: Ejecuta de manera periódica según el parámetro fetchInterval una función de la app de Vue definida para recoger el recuento de votos de la base de datos
         * Entrada: Ninguna
         * Salida: Ninguna
         */
        intervalFetch() {
            setInterval(() => {
                console.log(`Refrescando resultados de la votación: ${voting.id}`);
        
                this.app.getVotingCount().then(data => {
                    this.putOptionsValues(data);
                });
        
            }, this.fetchInterval);
        }

        /*
         * Descripción: recibe un recuento de votos, los filtra sumando cada votación por opción y actualiza la interfaz
         * Entrada: un fetch de la tabla VotingCount
         * Salida: Ninguna
         */
        putOptionsValues(fetch) {
            let categorizedVoting = this.categorizeVotingCount(fetch.votingCount);

            console.log(categorizedVoting);
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
            this.app.setOptions(this.options);
            this.app.setTotalVotes(this.totalVotes);
            this.app.setCensus(fetch.census);
            this.app.$forceUpdate();
        }

        /*
         * Descripción: recibe un recuento de votos y suma la cantidad de filas por cada respuesta a una opción de pregunta
         * Entrada: un fetch de la tabla VotingCount
         * Salida: Un array de objetos que identifican la opción de pregunta con la suma de las votaciones
         */
        categorizeVotingCount(votingCount) {
            let categorized = [],
                totalVotes = 0;

            for(let v of votingCount) {
                let option_id = v.option_id,
                    found = false;

                for(let i=0; i<categorized.length&&!found; i++) {
                    let c = categorized[i];

                    if(c.option_id==option_id) {
                        found = true;
                        c.count++;
                        totalVotes += 1;
                    }
                }
                if(!found) {
                    categorized.push({
                        ...v,
                        ...{
                            count: 1
                        }
                    });
                    totalVotes += 1;
                }
            }
            this.totalVotes = totalVotes;
            return categorized;
        }
    }

    new VotingCount(app, voting.question.options);
})();