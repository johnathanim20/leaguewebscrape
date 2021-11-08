function handleGetChamp(name) {
	var u = "http://127.0.0.1:5000/book?name=" +name
	console.log(u)
	fetch(u)
		.then(response => {
		console.log(response)
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
    		console.log(data)
				var counters = data.map(counterChamps => {
					temp = []
					for (x = 0; x < counterChamps.counter_champs.length; x++) {
						temp.push(`<p>counter_champs : ` + counterChamps.counter_champs[x]  + `</p>`)
					}
	                return temp
	            });
	            var strong = data.map(strongChamps => {
					temp = []
					for (x = 0; x < strongChamps.counter_champs.length; x++) {
						temp.push(`<p>strong_against : ` + strongChamps.strong_against[x]  + `</p>`)
					}
	                return temp2
	            });
				const html = data.map(champ => {
					var s = '<p>name : ' + champ.name + '</p>'
					+ '<p>win_rate : ' + champ.win_rate + '</p>'
					+ '<p>pick_rate : ' + champ.pick_rate + '</p>'
					+ '<p>champ_tier : ' + champ.champ_tier + '</p>'
					return s + temp + temp2;-
				});
		
			document.querySelector('#app').insertAdjacentHTML('afterbegin', html);
		}).catch(error=> {
			const returnObject = '<p>Error: ' + 'Not a valid name' + '</p>'
			document.querySelector('#app').insertAdjacentHTML('afterbegin', returnObject);
		});	
}