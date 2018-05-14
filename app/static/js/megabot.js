
$(document).ready(function(){
    $('.materialboxed').materialbox();
    $(".button-collapse").sideNav();
	$("#question").keypress(function(e){
		var key = e.which;
		if (key == 13) // the enter key code
		{
        submitQuestion();
		}
	});

	$("input:file").change(function(){
		upload_excel(this);
		this.value = '';
	});

	$(".sendQuestionButton").click(function() {
		$("#question").focus();
		<!--var e = jQuery.Event("keydown");-->
		<!--e.keyCode = 50;-->
		<!--$("#question").trigger(e);-->
		submitQuestion();
	});

	$(".downloadSampleExcel #download").click(function() {
		window.location.href = 'download/parameter_template.xlsx';
		message = "You are downloading the template for the parameters file, please use it to input your parameters.";
		showBotResponse(message);
    });

    $('.about').click(function() {
        $('.modal').openModal();
    });
});

var question_id = 1;
function upload_excel(input) {
    if (input.files && input.files[0]) {
        var formData = new FormData();
        formData.append('file', input.files[0]);
        $.ajax({
                type: 'POST',
                url: '/upload',
                data: formData,
                processData: false,
                contentType: false,
                success: function(response) {
                         excelHTML = response.excelHTML;
                         filename = response.filename;
                         request_status = response.request_status;
                         showBotResponse(request_status);
                         showExcelContent(excelHTML);
                         <!--window.location.href = 'downloadBI/'+filename-->
                         <!--console.log(response);-->
                },
        });
    }
}

function showExcelContent(excelHTML) {
	<!--$("#dragAndDropContentHeading").hide();-->
	var userChatDiv = $('<div class="row chatImage chat_row_human "></div>');
    var userColDiv = $('<div class="col s1000 m8000 l70 right"></div>');
    var userCardPanelDiv = $('<div class="card-panel right uploadedImageCard"></div>');
    var excelElement = $(excelHTML);
    $(userCardPanelDiv).prepend(excelElement);
    $(userColDiv).prepend(userCardPanelDiv);
    $(userChatDiv).prepend(userColDiv);
    $(".messages").append(userChatDiv);

    if ($(window).width() >= 600) {
		$(userChatDiv).scrollToFixed({
			marginTop: $(".nav-wrapper").innerHeight() + 5,
			zIndex: 500,
			unfixed: function() {
				$(userCardPanelDiv).removeClass("left");
				$(userCardPanelDiv).addClass("left");
			},
		});
    }
}


function submitQuestion() {
	var question = $("#question").val();
    if (question.length >= 1) {
        $("#question").val('');
        showUserQuestion(question);
        var formData = new FormData();
        formData.append('question', question);
        $.ajax({
				type: "POST",
				url: "/ask",
				data: {"messageText":question},
				success: function(response) {
						 var answer = response.answer;
						 showBotResponse(answer);
                         console.log(response);
				},
                error: function(error) {
                       console.log(error);
				}
        })
    }
}

function showUserQuestion(question) {
    var userChatDiv = $('<div class="row chat chat_row_human"></div>');
    var userColDiv = $('<div class="col s9 l7 right"></div>');
    var userCardPanelDiv = $('<div class="card-panel light-blue darken-4 right tooltipped" id="' + question_id + '"></div>');

    $(userCardPanelDiv).prepend('<span class="white-text">' + question + '</span>');
    $(userColDiv).prepend(userCardPanelDiv);
    $(userChatDiv).prepend(userColDiv);
    $(".messages").append(userChatDiv);

    $("html, body").animate({
        scrollTop: $(document).height()
    }, 100);
}

function showBotResponse(message) {
    var botChatDiv = $('<div class="row chat chat_bot_row"></div>');
    var botImage = $('<img src="static/images/MEGABOT.PNG" width="50px" height="50px" class="square" align="left">');
    var botColDiv = $('<div class="col s9 l7 left chat_bot"></div>');
    var botCardPanelDiv = $('<div class="card-panel black-text grey lighten-3"></div>');

    $(botCardPanelDiv).prepend('<span class="black-text">' + message + '</span>');
    $(botColDiv).prepend(botCardPanelDiv);
    $(botChatDiv).prepend(botColDiv);
    $(botChatDiv).prepend(botImage);
    $(".messages").append(botChatDiv);
    $("html, body").animate({
        scrollTop: $(document).height()
    }, 100);
}
