let theme = localStorage.getItem("theme")||"light"
const changeTheme = () => {
  if (theme == "light") {
    theme = "dark";
    document.body.style.backgroundColor = "black";

    localStorage.setItem("theme", "dark");
  } else if (theme == "dark") {
    theme = "light";

    document.body.style.backgroundColor = "rgb(230, 230, 230)";

    localStorage.setItem("theme", "light");
  }
};

