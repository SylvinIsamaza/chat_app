let theme = localStorage.getItem("theme") || "light";
console.log(theme)

const changeTheme = () => {
  if (theme == "light") {
    theme = "dark";
    document.body.style.backgroundColor = "black";
    elements = document.querySelectorAll('.bg-white')
    elements.forEach(function (element) {
      console.log('element')
      element.style.backgroundColor="#111111"; // Add class for changed style
    });

    localStorage.setItem("theme", "dark");
  } else if (theme == "dark") {
    theme = "light";

    document.body.style.backgroundColor = "rgb(230, 230, 230)";

    localStorage.setItem("theme", "light");
  }
};
const themeChanger = () => {
  console.log('Dom loaded fully')
  if (theme == "dark") {

    document.body.style.backgroundColor = "black";
    element = document.querySelectorAll('.bg-white')
    
  } else if (theme == "light") {
    document.body.style.backgroundColor = "rgb(230, 230, 230)";
  }
};
document.addEventListener("DOMContendLoaded", () => {
  console.log('Dom loaded successfully')
});
