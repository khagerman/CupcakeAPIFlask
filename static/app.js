const BASE_URL = "http://127.0.0.1:5000/api";

function showCupcakes(cupcake) {
  return `
<div data-id=${cupcake.id}>
<li>Flavor:<b>${cupcake.flavor}</b>
<ul>
      <li>Size: ${cupcake.size}</li>
      <li>${cupcake.rating}/5.0</li>
    </ul>
</li>
<img class="img-thumbnail" width="100" height="110""
            src="${cupcake.image}">
    
    
<button class="delete btn btn-danger btn-sm">X</button>`;
}
async function getCupcakes() {
  const res = await axios.get(`${BASE_URL}/cupcakes`);
  for (cupcake of res.data.cupcakes) {
    let newCupcake = showCupcakes(cupcake);
    $("#cupcakelist").append(newCupcake);
  }
}

$("#newcupcake").on("submit", async function (e) {
  e.preventDefault();
  let flavor = $("#flavor").val();
  let rating = $("#rating").val();
  let size = $("#size").val();
  let image = $("#image").val();
  const newCupcake = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image,
  });
  let addNewCupcake = showCupcakes(newCupcake.data.cupcake);
  $("#cupcakelist").append(addNewCupcake);
  $("#newcupcake").trigger("reset");
});
$("#cupcakelist").on("click", ".delete", async function (e) {
  e.preventDefault();
  let deleteCupcake = $(e.target).closest("div");
  let id = deleteCupcake.attr("data-id");
  await axios.delete(`${BASE_URL}/cupcakes/${id}`);
  deleteCupcake.remove();
});

$(getCupcakes);
