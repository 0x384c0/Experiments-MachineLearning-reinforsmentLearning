class Random{
	choice(choices){
		var index = Math.floor(Math.random() * choices.length);
		return choices[index];
	}
}

random = new Random()
np = nj

PI = Math.PI

function sin(num){
	return Math.sin(num)
}

function cos(num){
	return Math.cos(num)
}

function fract(x){
	return x - Math.floor(x)
}

function clamp(a,b,c){
	return Math.max(b,Math.min(c,a))
}

function int(float){
	if (float < 0)
		return Math.ceil(float)
	else
		return Math.floor(float)
}

function float(int){
	return int
}

function range(start,stop){
    if (stop == undefined)
        return [...Array(start).keys()]
    else
        return [...Array(stop - start).keys()].map(i => i + start)
}

function str(object){
	return object.toString()
}

function len(array){
	return array.length
}

function copy(obj){
	if (null == obj || "object" != typeof obj) return obj;
	var copy = new obj.constructor();
	for (var attr in obj) {
		if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
	}
	return copy;
}
function print(object){// override default print
	console.log(JSON.parse(JSON.stringify(object)))
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}