import WeatherCity from "./jsRu/createCity.js";
import CreateTips from "./jsRu/createTips.js";
const input = document.querySelector(".search-box__input");
const closeIcon = document.querySelector(".search-box__icon-close");
const searchBox = document.querySelector(".search-box");
const searchResult = document.querySelector(".search-result");
const resultList = document.querySelector(".search-result__list");
const resultItems = document.querySelector('.result__items');


LoadSaveCity("x");
let cityRu = [];
let cityKz = [];
CityRu();
CityKz();


resultItems.addEventListener("click", (event) => {
  if (event.target.closest('.delet-icon')) {
     let cityNameDelet = event.target.parentElement.id;
    DeleteCity(cityNameDelet);
    resultItems.removeChild(event.target.parentElement);
  }
 
});
function DeleteCity(name) {
  return fetch(`http://127.0.0.1:3000/api/cities/${name}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: name,
  })
};
function DeleteCityElement(city) {
  
}











resultList.addEventListener("click", (event) => {
  if (event.target.closest(".search-result__item")) {
    let currentCity = event.target.textContent;
    SearchDeleteActiveClass();
    GetCurrentWeather(currentCity);
    CloseIconOpacity();
  }
});

closeIcon.onclick = () => {
  input.value = "";
};

input.oninput = () => {
  CloseIconOpacity();
  resultList.innerHTML = "";
  let symbol = input.value;
  if (symbol === "") {
    SearchDeleteActiveClass();
    return;
  }
  CreateTips(symbol, cityRu);
  SearchAddActiveClass();
};

function CloseIconOpacity() {
  closeIcon.style.opacity = 1;
  if (input.value === "") {
    closeIcon.style.opacity = 0;
  }
}

function SearchDeleteActiveClass() {
  searchBox.classList.remove("search-box--active");
  searchResult.classList.remove("search-result--active");
}
function SearchAddActiveClass() {
  searchBox.classList.add("search-box--active");
  searchResult.classList.add("search-result--active");
}
function LoadSaveCity(x) {
  return fetch(`http://127.0.0.1:3000/api/cities/${x}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json;charset=utf-8",
    },
    body: "",
  })
    .then((res) => res.json())
    .then((c) => {
      for (const city of c) {
        GetCurrentWeather(city);
      }
    });
}
function CityRu() {
  return fetch(`http://127.0.0.1:3000/api/cities/ru`, {})
    .then((res) => res.json())
    .then((city) => {
      for (let i = 0; i < city.length; i++) {
        cityRu[i] = city[i];
      }
    });
}
function CityKz() {
  return fetch(`http://127.0.0.1:3000/api/cities/kz`, {})
    .then((res) => res.json())
    .then((city) => {
      for (let i = 0; i < city.length; i++) {
        cityKz[i] = city[i];
      }
    });
}
function GetCurrentWeather(city) {
  return fetch(`http://127.0.0.1:3000/api/main/${city}`, {
    headers: {
      "Content-type": "application/json; charset=UTF",
    },
  })
    .then((res) => res.json())
    .then((c) => {
      WeatherCity(c, city);
      CloseIconOpacity();
    });
}
