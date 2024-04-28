

$(document).ready(function () {
  var ascending = true;

  $("#sortByStatus").on("click", function () {
    var table = $("#employeelist");
    var rows = table.find("tbody > tr").get();

    rows.sort(function (a, b) {
      var keyA = $(a).find("td:eq(3)").text();
      var keyB = $(b).find("td:eq(3)").text();

      if (ascending) {
        return keyA.localeCompare(keyB);
      } else {
        return keyB.localeCompare(keyA);
      }
    });

    $.each(rows, function (index, row) {
      table.children("tbody").append(row);
    });

    ascending = !ascending;
  });
});

//Controls Table
$(document).ready(function () {
  var table = $("#controldetailstable").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: false,
    searching: true,
    lengthChange: false,
    pageLength: 20,
    initComplete: function () {
      this.api()
        .columns()
        .every(function () {
          var column = this;
          var header = $(column.header());
          var filterContainer = $(
            '<div class="filter-container" style="font-size:12px display="flex""></div>'
          ).appendTo($(header));
          var filter = $(
            '<input type="text" class="form-control form-control-sm" placeholder="" style="width:100%; font-size:12px" >'
          ).appendTo(filterContainer);
          filter.on("keyup change clear", function () {
            var val = $.fn.dataTable.util.escapeRegex($(this).val());
            column.search(val, true, false).draw();
          });
        });
    },
  });
});

//APP USERS TABLE
$(document).ready(function () {
  var table = $("#app_user_list").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: true,
    searching: true,
    lengthChange: false,
    pageLength: 10,
  });
  // Add an event listener to the search input
  $("#app_user_search_record").on("input", function () {
    table.search(this.value, false, false, false)
    .draw();
  });
});


//APP NEW USERS TABLE
$(document).ready(function () {
  var table = $("#app_new_user_table").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: true,
    searching: true,
    lengthChange: false,
    pageLength: 10,
    lengthMenu: [10, 20, 30, 50], 
    caseInsensitive: false, 
  });

  $("#app_user_new_user_search").on("input", function () {
    table.search(this.value, false, false, false)
    .draw();
  });

  // Add change event listener to the select box
  $("#app_user_new_user_status_filter").on("change", function () {
    var selectedStatus = $(this).val();
    table.column(2)
        .search(selectedStatus, false, false, false)
        .draw();
  }).on("keyup", function () {
    // This additional event listener is for handling case-sensitive search
    table.column(2)
        .search($(this).val(), false, false, false)
        .draw();
  });
});

//APP TERMINATED USERS TABLE
$(document).ready(function () {
  var table = $("#app_user_terminated_table").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: true,
    searching: true,
    lengthChange: false,
    pageLength: 10,
  });
  $("#app_user_termed_user_search").on("input", function () {
    table.search(this.value, false, false, false)
    .draw();
  });

 // Add change event listener to the select box
 $("#app_user_termed_user_status_filter").on("change", function () {
  var selectedStatus = $(this).val();
  table.column(2)
      .search(selectedStatus, false, false, false)
      .draw();
}).on("keyup", function () {
  // This additional event listener is for handling case-sensitive search
  table.column(2)
      .search($(this).val(), false, false, false)
      .draw();
});
});

//APP ADMIN USERS TABLE
$(document).ready(function () {
  var table = $("#app_user_admin_table").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: true,
    searching: true,
    lengthChange: false,
    pageLength: 10,
  });
  $("#app_user_admin_user_search").on("input", function () {
    table.search(this.value, false, false, false)
    .draw();
  });

 // Add change event listener to the select box
 $("#app_user_admin_user_status_filter").on("change", function () {
  var selectedStatus = $(this).val();
  table.column(2)
      .search(selectedStatus, false, false, false)
      .draw();
}).on("keyup", function () {
  // This additional event listener is for handling case-sensitive search
  table.column(2)
      .search($(this).val(), false, false, false)
      .draw();
});
});

//APP GENERIC USERS TABLE
$(document).ready(function () {
  var table = $("#app_user_generic_table").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: true,
    searching: true,
    lengthChange: false,
    pageLength: 10,
  });
  $("#app_user_generic_user_search").on("input", function () {
    table.search(this.value, false, false, false)
    .draw();
  });

 // Add change event listener to the select box
 $("#app_user_generic_user_status_filter").on("change", function () {
  var selectedStatus = $(this).val();
  table.column(2)
      .search(selectedStatus, false, false, false)
      .draw();
}).on("keyup", function () {
  // This additional event listener is for handling case-sensitive search
  table.column(2)
      .search($(this).val(), false, false, false)
      .draw();
});
});



//APP USERS MAPPED TO HR
$(document).ready(function () {
  var table = $("#app_user_mapped_table").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: true,
    searching: true,
    lengthChange: false,
    pageLength: 10,
  });
  $("#app_user_unmapped_search").on("input", function () {
    table.search(this.value, false, false, false)
    .draw();
  });
});

//APP USERS UNMAPPED TO HR
$(document).ready(function () {
  var table = $("#app_user_unmapped_table").DataTable({
    sDom: "lrtip",
    ordering: false,
    info: true,
    searching: true,
    lengthChange: false,
    pageLength: 10,
  });
  $("#app_user_mapped_search").on("input", function () {
    table.search(this.value, false, false, false)
    .draw();
  });
});