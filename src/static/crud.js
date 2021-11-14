//clears all the html results to be blank
function clear() {
	document.querySelector('#assesment').innerHTML = "";
}
//helper function to handle the parse of the array inputs
function parseArray(text) {
	const arr = text.split(",");
	for (var i = 0; i < arr.length; i++) {
		arr[i] = arr[i].trim();
	}
	return arr;
}

//handles the scrape button functionality
function scrape() {
	clear();
	url = "http://127.0.0.1:5000/scrape";
	const postMethod = {
		 method: 'POST',
		 headers: {
		  'Accept': 'application/json',
    	  'Content-Type': 'application/json'
		 }
	};
	fetch(url, postMethod)
		.then(response => {
			console.log(response);
			if (!response.ok) {
				throw ERROR("ERROR");
			}
			return response.text;
		})
		.then(data => {
		    const html = `<p>` + data + `</p>`;
		    document.querySelector('#assesment').insertAdjacentHTML('beforeend',html);
		})
		.catch(error => {
			console.log(error);
		});
}

//makes a put request to our API for the update button
// arr in order of winrate, pickrate, tier, counter champs, strong against champs
// fields array is there so we can create the proper key, value pair in the js object
// we need to specificly handle the array inputs
function update(name, arr) {
	clear();
	var tmpObject = {"name" : name};
	const fields = ["win_rate", "pick_rate", "champ_tier", "counter_champs", "strong_against"];
	for (var i = 0; i < arr.length; i++) {
		if (arr[i] != "") {
			if (fields[i] === "counter_champs" || fields[i] === "strong_against") {
				tmpObject[fields[i]] = parseArray(arr[i]);
			} else {
				tmpObject[fields[i]] = arr[i];
			}
		}
	}

	const putMethod = {
		 method: 'PUT',
		 headers: {
		  'Accept': 'application/json',
    	  'Content-Type': 'application/json'
		 },
		 body: JSON.stringify(tmpObject) // We send data in JSON format
	};
	url = "http://127.0.0.1:5000/champion?name=" + name;
	fetch(url, putMethod)
	.then(response => {
			console.log(response);
			if(!response.ok) {
				throw Error("ERROR");
			}
			return response.text();
		})
		.then(data => {
			console.log(data)
			if (data.error) {
				const b = `<p> ERROR: ` + data.message + `</p>`;
		    document.querySelector('#assesment').insertAdjacentHTML('beforeend',b);
		  } else {
		    const html = `<p>` + data + `</p>`;
		    document.querySelector('#assesment').insertAdjacentHTML('beforeend',html);
			}
		})
		.catch(error => {
			console.log(error);
		});
}
//function adds a new champion entry to our database
function create(arr) {
	clear();
	//checks if any parameters are empty strings
	var flag = 0;
	for (var i = 0; i < arr.length; i++) {
		if (arr[i] === "") {
			flag = 1;
			break;
		}
	}
	//error message to user
	if (arr.length < 6 || flag) {
		const b = `<p> ERROR: You did not fill out all forms!</p>`;
		document.querySelector('#assesment').insertAdjacentHTML('beforeend',b);
		return;
	}

	const tmpObject = {"name" : arr[0], "win_rate": arr[1], "pick_rate": arr[2], "champ_tier":arr[3], "counter_champs":arr[4], "strong_against":arr[5]};
	const postMethod = {
		 method: 'POST',
		 headers: {
		  'Accept': 'application/json',
    	  'Content-Type': 'application/json'
		 },
		  body: JSON.stringify(tmpObject)
	};
	const url = "http://127.0.0.1:5000/champion";

	fetch(url, postMethod)
	.then(response =>{
		if (!response.ok) {
			throw Error("error");
		}
		return response.json();
	})
	.then(data =>{
		if (data.status) {
			const b = `<p>` + data.message + `</p>`
			document.querySelector('#assesment').insertAdjacentHTML('beforeend',b);
		} else {
		const b = `<p> Created new Champ!</p>`

		document.querySelector('#assesment').insertAdjacentHTML('beforeend',b);
	}
	})
	.catch(error => {
		console.log(error);
	});
}
//delte function for our app
function del(name) {
	clear();
	url = "http://127.0.0.1:5000/champion?name=" + name;
	fetch(url, {method: 'DELETE'})
	.then(response => {
		if (!response.ok) {
			throw Error("error");
		}
		return response.text();
	})
	.then(data => {
		if (data.status) {
			const b = `<p>` + data.message + `</p>`
			document.querySelector('#assesment').insertAdjacentHTML('beforeend',b);
		} else {
			const b = `<p>` + data + `</p>`
			document.querySelector('#assesment').insertAdjacentHTML('beforeend',b);
		}
	}).catch(error => {
		console.log(error);
	});

}
