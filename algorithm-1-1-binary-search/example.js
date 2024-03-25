function binarySearch(inputs, start, end, target) {
  const mid = Math.floor((start + end) / 2);
  if (start > end) {
    return -1;
  }
  if (inputs[mid] === target) {
    return mid;
  }
  if (inputs[mid] < target) {
    return binarySearch(inputs, mid + 1, end, target);
  }
  return binarySearch(inputs, start, mid - 1, target);
}

function binarySearch2(inputs, start, end, target) {
  while (start <= end) {
    const mid = Math.floor((start + end) / 2);

    if (inputs[mid] === target) {
      return mid;
    } else if (inputs[mid] > target) {
      end = mid - 1;
    } else {
      start = mid + 1;
    }
  }

  return -1;
}

const inputs = [0, 0, 1, 2, 3, 3, 4, 5, 6, 6];
const result = binarySearch(inputs, 0, inputs.length - 1, 4);
const result2 = binarySearch2(inputs, 0, inputs.length - 1, 4);
console.log(result);
console.log(result2);
