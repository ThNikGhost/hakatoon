const resultItems = document.querySelector(".result__items");
const input = document.querySelector(".search-box__input");

export default function WeatherCity(city, cityName) {
  SaveCity(cityName);
  const cityItems = document.querySelectorAll(".result__item");
  let li_item = document.createElement("li");
  li_item.classList.add("result__item");
  li_item.id = cityName;

  let infoWrapper = CreateInfoWrapper(city, cityName);
  let weatherWrapper = CreateWeatherWrapper(city);
  let realFeel = CreateRealFeel(city);
  let deletIcon = document.createElement("div");
  deletIcon.classList.add("delet-icon");

  li_item.appendChild(infoWrapper);
  li_item.appendChild(weatherWrapper);
  li_item.appendChild(realFeel);
  li_item.appendChild(deletIcon);

  if (cityItems != null) {
    for (let i = 0; i < cityItems.length; i++) {
      if (cityItems[i].id === cityName) {
        input.value = "";

        input.placeholder = "Такой город уже добавлен";

        setTimeout(() => {
          input.placeholder = "Введите город";
        }, 1000);
        return;
      }
    }
  }

  if (resultItems.childElementCount > 2) {
    let deletElement = document.querySelectorAll(".result__item")[0];
    deletElement.classList.add("delet-city");

    setTimeout(() => {
      resultItems.removeChild(deletElement);
      li_item.classList.add("add-city");
      resultItems.appendChild(li_item);
    }, 500);
  } else {
    li_item.classList.add("fist-add");
    resultItems.appendChild(li_item);
    setTimeout(() => {
      li_item.classList.remove("fist-add");
    }, 1000);
  }
  input.value = "";
}

function CreateInfoWrapper(city, cityName) {
  let info_wrapper = document.createElement("div");
  info_wrapper.classList.add("city-info__wrapper");
  let city_name = document.createElement("div");
  city_name.classList.add("city-name");
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
  weather_icon.src = `http://openweathermap.org/img/w/${city.icon}.png`;
  let temp = document.createElement("span");
  temp.classList.add("city-temp");
  temp.textContent = Math.floor(city.temp) + "°";
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
  feel_value.textContent = " " + Math.floor(city.temp_feels) + "°";
  real_feel.appendChild(feel_value);

  return real_feel;
}

function SaveCity(cityName) {
  return fetch(`http://127.0.0.1:3000/api/cities/${cityName}`, {
    method: "POST",
    body: cityName,
  });
}
