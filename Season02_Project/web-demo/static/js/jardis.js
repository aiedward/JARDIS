(function() {
    const $story        = $('#story'),
          $question     = $('#question'),
          $answer       = $('#answer'),
          $getAnswer    = $('#get_answer'),
          $getStory     = $('#get_story'),
          $explainTable = $('#explanation')

    // Activate tooltip
    $('.qa-container').find('.glyphicon-info-sign').tooltip()

    $getAnswer.on('click', function(e) {
        e.preventDefault()
        getAnswer()
    })

    $getStory.on('click', function(e) {
        e.preventDefault()
        getStory()
    })

    function getStory() {
        $.get('/get/story', function(dataObj) {
            $('#story').remove()
            $('.story-form-group').append('<div id="story"></div>')
            const words_elements = dataObj['story'].split(' ').map((el) => {
              let result = `<span>${ el }</span> `
              if (el.includes('.')) {
                  result += '<br>'
              }
              return result
            })
            for (let i = 0; i < words_elements.length; i++) {
              $('#story').append(words_elements[i])
            }

            $question.val(dataObj["question"])
            $question.data('question_idx', dataObj["question_idx"])
            $question.data('suggested_question', dataObj["question"])
            $answer.val('')
            $answer.data('correct_answer', dataObj["correct_answer"])
        })
    }

    function getAnswer() {
        const questionIdx       = $question.data('question_idx'),
            correctAnswer     = $answer.data('correct_answer'),
            suggestedQuestion = $question.data('suggested_question'),
            question          = $question.val()

        const userQuestion = suggestedQuestion !== question? question : ''
        const url = `/get/answer?question_idx=${ questionIdx }&user_question${ encodeURIComponent(userQuestion) }`

        $.get(url, function(dataObj) {
            const predAnswer = dataObj["pred_answer"]
            const predProb = dataObj["pred_prob"]
            const outputMessage = `Answer = '${ predAnswer }'\nConfidence score = ${ (predProb * 100).toFixed(2) }%`

            // Show answer's feedback only if suggested question was used
            if (userQuestion === '') {
                if (predAnswer === correctAnswer)
                    outputMessage += "\nCorrect!"
                else
                    outputMessage += "\nWrong. The correct answer is '" + correctAnswer + "'"
            }
            $answer.val(outputMessage)
        })
    }

    getStory()
})()
