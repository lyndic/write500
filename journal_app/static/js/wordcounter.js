function wordCount(count) {
    var count;
    var words = count.split(/\b\s/g);
    count = words.length;
    
    var element = document.getElementById('totalCount');
    element.value = count;

    document.getElementById('totalCount').innerHTML = element;
}

function wordGoals(count) {
    var count;
    
    if (count > 500) {
        alert('Congratulations! You have met your daily goal!')
    }
    else if (count > 1000) {
        alert('You are a writing master!')
    }
}