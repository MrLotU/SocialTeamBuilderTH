$( document ).ready(function() {

  $('textarea').autogrow({onInitialize: true});

  function updateElementIndex(el, ndx) {
    var regex = /formset-\d+/
    var replacement = 'formset-' + ndx
    if ($(el).attr('for')) $(el).attr('for', $(el).attr('for').replace(regex, replacement))
    if (el.id) el.id = el.id.replace(regex, replacement)
    if (el.name) el.name = el.name.replace(regex, replacement)
  }

  function updateElementIndices() {
    var forms = $('.form-row')
    console.log(forms.length);
    for (var i=0; i<forms.length; i++) {
      $(forms.get(i)).find(':input').each(function() {
        updateElementIndex(this, i)
      })
    }
  }

  //Cloner for infinite input lists
  $(".circle--clone--list").on("click", ".circle--clone--add", function(){
    var parent = $(this).parent("li");
    var copy = parent.clone();
    parent.after(copy);
    copy.find("input, textarea, select").val("");
    copy.find("*:first-child").focus();
    var total = $('#id_formset-TOTAL_FORMS').val()
    if (total === undefined) { return }
    copy.find(':input').each(function() {
      var name = $(this).attr('name').replace(/-\d+-/, '-' + total + '-');
      var id = 'id_' + name;
      $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    })
    total++
    $('#id_formset-TOTAL_FORMS').val(total)
    updateElementIndices()
  });

  $(".circle--clone--list").on("click", "li:not(:only-child) .circle--clone--remove", function(){
    var parent = $(this).parent("li");
    parent.remove();
    var total = $('#id_formset-TOTAL_FORMS').val()
    if (total === undefined) { return }
    total--
    $('#id_formset-TOTAL_FORMS').val(total)
    updateElementIndices()
  });

  // Adds class to selected item
  $(".circle--pill--list a").click(function() {
    $(".circle--pill--list a").removeClass("selected");
    $(this).addClass("selected");
  });

  // Adds class to parent div of select menu
  $(".circle--select select").focus(function(){
   $(this).parent().addClass("focus");
   }).blur(function(){
     $(this).parent().removeClass("focus");
   });

  // Clickable table row
  $(".clickable-row").click(function() {
      var link = $(this).data("href");
      var target = $(this).data("target");

      if ($(this).attr("data-target")) {
        window.open(link, target);
      }
      else {
        window.open(link, "_self");
      }
  });

  // Custom File Inputs
  var input = $(".circle--input--file");
  var text = input.data("text");
  var state = input.data("state");
  input.wrap(function() {
    return "<a class='button " + state + "'>" + text + "</div>";
  });




});