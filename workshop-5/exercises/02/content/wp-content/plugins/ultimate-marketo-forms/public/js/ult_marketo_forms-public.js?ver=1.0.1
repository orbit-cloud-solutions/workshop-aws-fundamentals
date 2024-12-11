function readCookie(name) {
  var cookiename = name + "=";
  var ca = document.cookie.split(";");
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == " ") c = c.substring(1, c.length);
    if (c.indexOf(cookiename) == 0)
      return c.substring(cookiename.length, c.length);
  }
  return null;
}

function get_url_var(parameterName) {
  var result = null,
    tmp = [];
  location.search
    .substr(1)
    .split("&")
    .forEach(function(item) {
      tmp = item.split("=");
      if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    });
  return result;
}

function form_ready(form) {
  var fields = new Array();
  jQuery("#mktoForm_" + form.getId() + " :input").each(function() {
    var name = jQuery(this).prop("name");
    if (name > "" && name != "s" && name != "munchkinId" && name != "formid")
      fields.push(name);
  });
  if (typeof plugin_path !== 'undefined') {
    jQuery.post(
      plugin_path,
      {
        action: "mrkto_check_lead",
        form_id: form.getId(),
        fields: fields,
        filterValues: readCookie("_mkto_trk")
      },
      function(response) {
        var json = jQuery.parseJSON(response);
        if (json.status == "success") {
          mktoLeadFields = json.info;

          var prefillFields = {};
          jQuery("#mktoForm_" + form.getId() + " :input").each(function() {
            for (var o2 in mktoLeadFields) {
              var name = jQuery(this)
                .prop("name")
                .toLowerCase();
              var name2 = o2.toLowerCase();
              if (
                name2 == name &&
                name > "" &&
                name != "s" &&
                name != "munchkinId" &&
                name != "formid"
              ) {
                if (
                  jQuery(this).prop("type") == "checkbox" ||
                  jQuery(this).prop("type") == "radio"
                ) {
                  if (
                    mktoLeadFields[o2] == jQuery(this).val() ||
                    mktoLeadFields[o2] == true
                  ) {
                    jQuery(
                      "#mktoForm_" +
                        form.getId() +
                        " input[name=" +
                        jQuery(this).prop("name") +
                        "]"
                    ).prop("checked", true);
                    //console.log('set '+jQuery(this).prop('name')+' to checked');
                  }
                } else {
                  jQuery(
                    "#mktoForm_" +
                      form.getId() +
                      " input[name=" +
                      jQuery(this).prop("name") +
                      "]"
                  ).val(mktoLeadFields[o2]);
                  //console.log('set '+jQuery(this).prop('name')+' to '+mktoLeadFields[o2]);
                }
              }
            }
          });

          window["update_umrktofrm_" + form.getId() + "_fields"](form.getId());
        } else console.log(json.reason);
      }
    );
  }
}

(function($) {
  "use strict";

  MktoForms2.whenReady(function(form) {
    form_ready(form);
  });
})(jQuery);
