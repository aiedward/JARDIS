var func = function() {
    var $story        = $('#story'),
        $question     = $('#question'),
        $answer       = $('#answer'),
        $getAnswer    = $('#get_answer'),
        $getStory     = $('#get_story'),
        $explainTable = $('#explanation');

    getStory();

    // Activate tooltip
    $('.qa-container').find('.glyphicon-info-sign').tooltip();

    $getAnswer.on('click', function(e) {
        e.preventDefault();
        getAnswer();
    });

    $getStory.on('click', function(e) {
        e.preventDefault();
        getStory();
    });

    function getStory() {
        $.get('/get/story', function(json) {
            $story.val(json["story"]);
            $question.val(json["question"]);
            $question.data('question_idx', json["question_idx"]);
            $question.data('suggested_question', json["question"]); // Save suggested question
            $answer.val('');
            $answer.data('correct_answer', json["correct_answer"]);
        });
    }

    function getAnswer() {
        var questionIdx       = $question.data('question_idx'),
            correctAnswer     = $answer.data('correct_answer'),
            suggestedQuestion = $question.data('suggested_question'),
            question          = $question.val();

        var userQuestion = suggestedQuestion !== question? question : '';
        var url = '/get/answer?question_idx=' + questionIdx +
            '&user_question=' + encodeURIComponent(userQuestion);

        $.get(url, function(json) {
            var predAnswer = json["pred_answer"], predProb = json["pred_prob"]
                //memProbs = json["memory_probs"];

            var outputMessage = "Answer = '" + predAnswer + "'" + "\nConfidence score = " + (predProb * 100).toFixed(2) + "%";

            // Show answer's feedback only if suggested question was used
            if (userQuestion === '') {
                if (predAnswer === correctAnswer)
                    outputMessage += "\nCorrect!";
                else
                    outputMessage += "\nWrong. The correct answer is '" + correctAnswer + "'";
            }
            $answer.val(outputMessage);
        });
    }
};
$(document).ready(func)
