
fetch("products.json")
.then(function(response){
	return response.json();
})
.then(function(products){
	let placeholder = document.querySelector("#data-output");
	let out = "";
	for(let product of products){
		out += `
			<tr>
				<td colspan="3" class="quest-num">Question ${product.id}</td>
			</tr>
			<tr>
				<td colspan="2" style="font-weight: bold">
				${product.question}
				</td>
			</tr>
			<tr>
				<td colspan="2">
				${product.answer}
				</td>
			</tr>
		`;
	}

	placeholder.innerHTML = out;
});