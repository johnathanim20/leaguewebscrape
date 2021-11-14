function handleGetChamp(name) {
	console.log(name)
	var u = "http://127.0.0.1:5000/champion?name="+name
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
					temp2 = []
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
					return s + temp + temp2;
				});
			document.querySelector('#championGet').innerHTML = "";
			document.querySelector('#championGet').insertAdjacentHTML('afterbegin', html);
		}).catch(error=> {
			const returnObject = '<p>Error: ' + 'Not a valid name' + '</p>'
			document.querySelector('#championGet').insertAdjacentHTML('afterbegin', returnObject);
		});
}

function handleGetQuery(querystring) {
	var u = "http://127.0.0.1:5000/search?q=" + querystring
	console.log(u)
	var dict = [];
	fetch(u)
		.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
			console.log(data)
			for (x = 0; x < data.result.length; x++) {
				var counters = data.result.map(counterChamps => {
					temp = []
					for (x = 0; x < counterChamps.counter_champs.length; x++) {
						temp.push(`<p>counter_champs : ` + counterChamps.counter_champs[x]  + `</p>`)
					}
	                return temp
	            });
	            var strong = data.result.map(strongChamps => {
					temp2 = []
					for (x = 0; x < strongChamps.counter_champs.length; x++) {
						temp.push(`<p>strong_against : ` + strongChamps.strong_against[x]  + `</p>`)
					}
	                return temp2
	            });
				const html = data.result.map(champ => {
					var s = '<p>name : ' + champ.name + '</p>'
					+ '<p>win_rate : ' + champ.win_rate + '</p>'
					+ '<p>pick_rate : ' + champ.pick_rate + '</p>'
					+ '<p>champ_tier : ' + champ.champ_tier + '</p>'
					return s + temp + temp2;
				});
				document.querySelector('#championGet').innerHTML = "";
				document.querySelector('#championGet').insertAdjacentHTML('afterbegin', html);
			}
		}).catch(error=> {
			console.log(error)
			const returnObject = '<p>Error: ' + 'Not a valid name' + '</p>'
			document.querySelector('#championGet').insertAdjacentHTML('afterbegin', returnObject);
		});
}

function query(querystring) {
	clearValues();
	var u = "http://127.0.0.1:5000/search?q=" + querystring
	console.log(u)
	var dict = [];
	fetch(u)
		.then(response => {
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
				if (data.status) {
					const b = `<p>` + data.message + `</p>`
					document.querySelector('#championGet').insertAdjacentHTML('beforeend',b);
				} else {

					const html = data.result.map(champ => {
						dict.push({
						name : champ.name,
						win_rate : champ.win_rate,
						pick_rate : champ.pick_rate,
						champ_tier : champ.champ_tier,
						counter_champs:champ.counter_champs,
						strong_against:champ.strong_against
						})
					});
					addTable(dict)
			}
		})
}

function getChamp(name) {
	clearValues();
	console.log(name)
	var u = "http://127.0.0.1:5000/champion?name="+name
	console.log(u)
	var dict = [];
	fetch(u)
		.then(response => {
		console.log(response)
			if (!response.ok) {
				throw Error("ERROR");
			}
			return response.json();
    	}).then(data=> {
				console.log(data[0])
				if (data[0].status) {
					const b = `<p>` + data[0].message + `</p>`
					document.querySelector('#championGet').insertAdjacentHTML('beforeend',b);
				} else {
    			console.log(data);
    			const html = data.map(champ => {
					dict.push({
					name : champ.name,
					win_rate : champ.win_rate,
					pick_rate : champ.pick_rate,
					champ_tier : champ.champ_tier,
					counter_champs:champ.counter_champs,
					strong_against:champ.strong_against
					})
				});
				addTable(dict)
			}
		})
}

function addTable(arr2) {
  arr = arr2

  	  document.querySelector('#myDynamicTable').innerHTML = "";
	  var myTableDiv = document.getElementById("myDynamicTable");

	  var table = document.createElement('TABLE');
	  table.border = '1';
	  const a = ["name","pick_rate","win_rate","champ_tier","counter_champs","strong_against"];


	  var tableBody = document.createElement('TBODY');
	  table.appendChild(tableBody);

	  var tr = document.createElement('TR');
	  tableBody.appendChild(tr);
	  for (var j = 0; j < 6; j++) {
		  var td = document.createElement('TD');
		  td.width = '75';
		  td.appendChild(document.createTextNode(a[j]));
		  tr.appendChild(td);
	  }


	  for (var i = 0; i < arr.length; i++) {
	    var tr = document.createElement('TR');
	    tableBody.appendChild(tr);
	    for (var j = 0; j < 6; j++) {
	      var td = document.createElement('TD');
	      td.width = '75';

	      td.appendChild(document.createTextNode(arr[i][a[j]]));
	      tr.appendChild(td);
	    }
	  }
	  myTableDiv.appendChild(table);

}


function clearValues() {
	document.querySelector('#myDynamicTable').innerHTML = "";
	document.querySelector('#championGet').innerHTML = "";
}
