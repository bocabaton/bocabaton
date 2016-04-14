var BpmnJS = window.BpmnJS;

var bpmnjs = new BpmnJS({ container: '#bpmn' });

function success() {
  $('body').addClass('success');
}

function fail(err) {
  $('body').addClass('fail');

  console.error('something went wrong!');
  console.error(err);
}

$.get('/admin/assets/resources/devops.bpmn', function(pizzaDiagram) {

  bpmnjs.importXML(pizzaDiagram, function(err) {

    if (err) {
      return fail(err);
    }

    try {
      //bpmnjs.get('bpmn').zoom('fit-viewport');
      return success();
    } catch (e) {
      return fail(e);
    }
  });

}, 'text');
