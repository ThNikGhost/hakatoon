const btn = document.querySelector(".get");
const input = document.querySelector(".search-box__input");
const closeIcon = document.querySelector(".search-box__icon-close");
const searchBox = document.querySelector(".search-box");
const searchResult = document.querySelector(".search-result");
const resultList = document.querySelector(".search-result__list");
const resultItems = document.querySelector(".result__items");

let cityName = '';
let tempValue = '';
let tempFeel = '';


let currentCity = [];
let cityRu = [];
CityRu();
function CityRu() {
  return fetch(`http://127.0.0.1:3000/api/cities/ru`, {})
    .then((res) => res.json())
    .then((city) => {
      for (let i = 0; i < city.length; i++) {
        cityRu[i] = city[i];
      }
    });
}

resultList.addEventListener("click", (event) => {
  if (event.target.closest(".search-result__item")) {
    let currentCity = event.target.textContent;
    console.log(currentCity);
    GetCurrentWeather(currentCity);

    
  }
});

function GetCurrentWeather(city) {
  return fetch(`http://127.0.0.1:3000/api/main/${city}`, {
    headers: {
      "Content-type": "application/json; charset=UTF",
    },
  })
    .then((res) => res.json())
    .then((c) => {
      console.log(c);
      WeatherCity(c, city);
    });
}

input.oninput = () => {
  CloseIconOpacity();
  ClearSearchCity();
  let symbol = input.value;
  if (symbol === "") {
    SearchDeleteActiveClass();
    return;
  }
  CreateTips(symbol);
  SearchAddActiveClass();
};
// input.onblur = () => {
//   SearchDeleteActiveClass();
// };

function CloseIconOpacity() {
  closeIcon.style.opacity = 1;
  if (input.value === "") {
    closeIcon.style.opacity = 0;
  }
}
function CreateTips(symbol) {
  currentCity = cityRu.filter(function (city) {
    return city.toLowerCase().startsWith(`${symbol.toLowerCase()}`);
  });
  for (const city of currentCity) {
    CreateSearchCity(city);
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
function ClearSearchCity() {
  resultList.innerHTML = "";
}
function CreateSearchCity(city) {
  let li = document.createElement("li");
  li.classList.add("search-result__item");
  li.textContent = `${city}`;
  resultList.appendChild(li);
}

function WeatherCity(city, cityName) {
  let li_item = document.createElement("li");
  li_item.classList.add("result__item");

  let infoWrapper = CreateInfoWrapper(city,cityName);
  let weatherWrapper = CreateWeatherWrapper(city);
  let realFeel = CreateRealFeel(city);

  li_item.appendChild(infoWrapper);
  li_item.appendChild(weatherWrapper);
  li_item.appendChild(realFeel);

  resultItems.appendChild(li_item);
}

function CreateInfoWrapper(city,cityName) {
  let info_wrapper = document.createElement("div");
  info_wrapper.classList.add("city-info__wrapper");
  let city_name = document.createElement("div");
  city_name.classList.add("city-name");
  console.log(cityName);
  city_name.textContent = cityName;
  let country = document.createElement("div");
  country.classList.add("city-country");
  country.textContent = "Казахстан";

  info_wrapper.appendChild(city_name);
  info_wrapper.appendChild(country);

  return info_wrapper;
}
function CreateWeatherWrapper(city) {
  let weather_wrapper = document.createElement("div");
  weather_wrapper.classList.add("city-weather__wrapper");

  let weather_icon = document.createElement("img");
  weather_icon.classList.add("weather-icon");
  weather_icon.src = "../static/img/weather.png";
  let temp = document.createElement("span");
  temp.classList.add("city-temp");
  temp.textContent = Math.floor(city.temp)  + "°";
  let unit = document.createElement("span");
  unit.classList.add("temp-unit");
  unit.textContent = " C ";
  temp.appendChild(unit);

  weather_wrapper.appendChild(weather_icon);
  weather_wrapper.appendChild(temp);

  return weather_wrapper;
}
function CreateRealFeel(city) {
  let real_feel = document.createElement("div");
  real_feel.classList.add("real-feel");
  real_feel.textContent = "Ощущается как";
  let feel_value = document.createElement("span");
  feel_value.classList.add("real-feel__value");
  feel_value.textContent = " " + city.temp_feels + "°";
  real_feel.appendChild(feel_value);

  return real_feel;
}
