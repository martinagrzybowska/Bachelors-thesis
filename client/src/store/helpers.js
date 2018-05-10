/* Helper function for prepping the path to server */
export function tidyURL(path) {  
	if (path.charAt(0) == '/') {
		path = path.slice(1);
	}
	if (path.charAt(path.length - 1) == '/') {
		path = path.slice(0, path.length - 1);
	}

	return path
}