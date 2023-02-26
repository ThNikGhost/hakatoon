const resultList = document.querySelector(".search-result__list");
let currentCity = [];

function CreateTips(symbol, cityRu) {
  currentCity = cityRu.filter(function (city) {
    return city.toLowerCase().startsWith(`${symbol.toLowerCase()}`);
  });
  for (const city of currentCity) {
    CreateSearchCity(city);
  }
}

function CreateSearchCity(city) {
  let li = document.createElement("li");
  li.classList.add("search-result__item");
  li.textContent = `${city}`;
  resultList.appendChild(li);
}

export default CreateTips;
