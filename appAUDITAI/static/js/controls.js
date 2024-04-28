//Code to retreive tabs and activate on page load
$(document).ready(function () {
  var tabs = JSON.parse(localStorage.getItem("tabs")) || {};
  for (var tabId in tabs) {
    var tab = tabs[tabId];
    var tabName = tab.name;
    // Create a new tab with the saved tab ID and name
    var newTabLink = $(
      '<a class="nav-link dynamic-tab-link" data-process-id="" data-bs-toggle="tab" data-bs-target="#' +
        tabId +
        '" style="background-color:#4B5F74;color:white;font-size:12px;height:38px;">' +
        tabName +
        '<button type="button" class="btn-close close-tab" style="font-size:8px;margin-left:10px;" aria-label="Close"></button></a>'
    );
    var newTab = $('<li class="nav-item"></li>').append(newTabLink);
    $(".nav-tabs").append(newTab);

    // Clone the #template div, remove its ID and hidden attributes, and add it to the new tab
    var newContent = $("#template")
      .clone()
      .removeAttr("id")
      .removeAttr("style");

    var newTabContent = $(
      '<div class="tab-pane fade" id="' + tabId + '"></div>'
    ).append(newContent.html());

    // Append the new tab content to the first tab
    if ($.isEmptyObject(tabs)) {
      $(".tab-content").append(newTabContent);
    }

    // Append the new tab content to the new tab
    else {
      $(".tab-content").append(newTabContent);
    }

    newTab.find(".close-tab").click(function () {
      var tab = $(this).closest(".nav-item");
      var contentId = $(this).parent().attr("data-bs-target");
      var content = $(contentId);
      tab.remove();
      content.remove();

      // Remove the tab from local storage
      delete tabs[contentId.substring(1)];
      localStorage.setItem("tabs", JSON.stringify(tabs));
    });
  }

  var savedTab = localStorage.getItem("selectedTabId");
  if (savedTab) {
    $(".nav-tabs li a").each(function () {
      if ($(this).text() === savedTab) {
        $(this).tab("show");
      }
    });
  }
});

//Code to reload page on click
$(document).on("click", ".dynamic-tab-link", function () {
  var selectedTab = $(this).text();
  localStorage.setItem("selectedTabId", selectedTab);
  var tabs = JSON.parse(localStorage.getItem("tabs")) || {};
  for (var tabId in tabs) {
    var tab = tabs[tabId];
    var tabName = tab.name;
    if (tab.name === selectedTab) {
      var controlID = tab.field2;
      var projectId = localStorage.getItem("project_id");
      var newUrl = "/controlform/" + projectId + "/" + controlID;
      // Switch to the selected tab first
      $(this).tab("show");
      // Load the new page after switching tabs
      window.location.href = newUrl;
      break; // Stop iterating through the tabs once a match is found
    }
  }
});

$('#controls-link').click(function() {
  var projectId = localStorage.getItem("project_id");
  window.location.href = '/allcontrols/' + projectId + '/' + '0/'
  
  // You can navigate to the link using:
  // window.location.href = $('#controls-link').attr('href');
});

$('.carousel').on('click', function() {
  $('.carousel').removeClass('active');
  $(this).addClass('active');
});