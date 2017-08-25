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
            $('#story').attr('question_idx', dataObj['question_idx'].toString())

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

            $('#question').val(dataObj['question'])
            $answer.val('')
            $answer.data('correct_answer', dataObj['correct_answer'])
        })
    }

    function getAnswer() {
        const questionIdx       = parseInt($('#story').attr('question_idx'))
        const correctAnswer     = $('#answer').data('correct_answer')
        const url               = `/get/answer?question_idx=${ questionIdx }`

        $.get(url, function(dataObj) {
          const predAnswer = dataObj['pred_answer']
          const predProb = dataObj['pred_prob']
          const word2idx = dataObj['word2idx']
          const predProbAll = dataObj['pred_prob_all']

          let outputMessage = `Answer = '${ predAnswer }'\nConfidence score = ${ (predProb * 100).toFixed(2) }%\n`
          if (predAnswer === correctAnswer)
            outputMessage += 'Correct!'
          else
            outputMessage += `Wrong. The correct answer is '${ correctAnswer }'`
          $('#answer').val(outputMessage)

          const c = $('#story').children()
        //  for (let i = 0; i < c.length; i++) {
        //    const p = predProbAll[word2idx[c[i].innerText]]
        //    if (p && p > 0.3) {
        //      c[i].setAttribute("style",`background-color: rgba(255, 255, 0, ${ p }`)
        //    }
        //  }

          for (let i = c.length - 1; i >= 0; i--) {
            const p = predProbAll[word2idx[c[i].innerText]]
            if (c[i].innerText === correctAnswer) {
              c[i].setAttribute("style", `background-color: rgba(255, 255, 0, ${ p })`)
              break
            }
          }
        })
    }

    getStory()
})()
