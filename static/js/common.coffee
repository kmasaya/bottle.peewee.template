$(document).ready(->
  $('a[rel*=leanModal]').leanModal(
    closeButton: ".modal_close"
  )
)