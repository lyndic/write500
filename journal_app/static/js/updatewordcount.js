function updateWordCount (count) {
    console.log('It works!')
    var count;
    var words = count.split(/\S+/g);
    count = words.length - 1;

    var element = document.getElementById('totalCount');
    element.value = count;
    document.getElementById('totalCount').innerHTML = element;
}