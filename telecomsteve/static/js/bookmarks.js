// this file holds scripting used by the bookmarks page

function showPopup() {
    var popupContainer = document.getElementById("popupContainer");
    popupContainer.style.display = "flex";
  
    // Clear input fields
    document.getElementById("itemText").value = "";
    document.getElementById("destination").value = "";
    document.getElementById("imageUrl").value = "";
  }
  
  function hidePopup() {
    var popupContainer = document.getElementById("popupContainer");
    popupContainer.style.display = "none";
  }
  
  function addGridItem() {
    var itemText = document.getElementById("itemText").value;
    var destination = document.getElementById("destination").value;
    var imageUrl = document.getElementById("imageUrl").value;
  
    if (itemText && destination) {
      var newGridItem = document.createElement("div");
      newGridItem.className = "grid-item";
      newGridItem.innerText = itemText;
  
      if (imageUrl) {
        newGridItem.style.backgroundImage = `linear-gradient(45deg, #ffeb3b, #9c27b0), url('${imageUrl}')`;
      } else {
        newGridItem.style.backgroundImage = `linear-gradient(45deg, #ffeb3b, #9c27b0)`; /* Default color if no image URL is provided */
      }
  
      // Open destination URL on click
      newGridItem.onclick = function () {
        window.open(destination, "_blank");
      };
  
      var gridContainer = document.getElementById("gridContainer");
      var plusIcon = gridContainer.lastElementChild;
      gridContainer.insertBefore(newGridItem, plusIcon);
  
      hidePopup();
    } else {
      alert("Please enter all required fields.");
    }
  }
  