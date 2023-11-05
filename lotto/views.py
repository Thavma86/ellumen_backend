from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['POST'])
def find_counter(request):

    if request.method == 'POST':
        result = []
        checked = []

        # Get data from users
        num1 = request.data.get('num1')
        num2 = request.data.get('num2')
        num3 = request.data.get('num3')
        num4 = request.data.get('num4')
        num5 = request.data.get('num5')

        winning_numbers = [num1, num2, num3, num4, num5]
        all_counters = []
        
        # zig zag subtractions
    zig_zag_subtracted_winning_nums = []
    def zig_zag_subtractions(winning_numbers):
        subtracted_nums_array = []
        subtracted_num = winning_numbers[0]
        for nums in winning_numbers[1:]:
            subtracted_num = subtracted_num - nums if subtracted_num > nums else nums - subtracted_num
        subtracted_nums_array.append(subtracted_num)
        return subtracted_nums_array
    
    get_zigz_zag_subtractions = zig_zag_subtractions(winning_numbers)
    zig_zag_subtracted_winning_nums.extend(get_zigz_zag_subtractions)

    
    all_counters = []
    initial_counter = 45

    # Counter function
    def find_counters(winning_numbers):
        matching_counters = []
        for nums in winning_numbers:
            counter = initial_counter
            if nums <= counter:
                matching_counter = nums + counter
            else:
                matching_counter = nums - counter
            matching_counters.append(matching_counter)
        return matching_counters
    
    # Find counters function is called
    match_counters = find_counters(winning_numbers)
    all_counters.extend(match_counters)
    print(f"All Counters: {all_counters}")
    
    first_num = winning_numbers[0]
    last_num = zig_zag_subtracted_winning_nums[-1]
    
    
    if last_num <= initial_counter:
        modified = last_num + initial_counter
    else:
        modified = last_num - initial_counter

    final_first_num = first_num - modified  # Adjusted addition
    
    if final_first_num <= initial_counter:
        first_num_counter = final_first_num + initial_counter
    else:
        first_num_counter = final_first_num - initial_counter

    processed_result = f"{final_first_num}/{first_num_counter}"
    print(f"Processed Result:", processed_result)

    # Straight line subtractions function
    def straight_line_subtractions(winning_numbers):
        straight_line_subtracted_array = []
        for idx, item in enumerate(winning_numbers):
            total_list_array = []
            for x in winning_numbers[idx + 1:]:
                total = item - x
                total_list_array.append(total)
            straight_line_subtracted_array.extend(total_list_array)
        return straight_line_subtracted_array
    
        
    all_straight_subtracted_array = straight_line_subtractions(winning_numbers)
    print(f"All Stright line Subtracted Array: {all_straight_subtracted_array}")

    # ensure all numbers are positive
    list2_ab = set(abs(value) for value in all_straight_subtracted_array)
    # Function to check for matches
    def find_match(value):
        is_match = []
        if abs(value) in list2_ab:
            is_match.append(value)
        return is_match


    # messages = []
    # for value in all_straight_subtracted_array:
    #     matches = find_match(value)
    #     if matches:
    #         print(f"There is a match for {value}.")
    #     else:
    #         print(f"No match found for {value}")



    return Response({'message': processed_result})
