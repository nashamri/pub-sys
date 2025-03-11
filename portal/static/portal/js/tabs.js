document.addEventListener("DOMContentLoaded", function () {
  // Function to handle single tab scenario
  function handleSingleTab() {
    const tabNav = document.getElementById("tab-nav");
    const tabs = tabNav.getElementsByClassName("tab-link");

    if (tabs.length === 1) {
      tabs[0].classList.add("w-full");
      tabs[0].classList.remove("flex-1");
    }
  }

  // Call on page load
  handleSingleTab();
});
