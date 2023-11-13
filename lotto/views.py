from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


def user_input_nums(num1, num2, num3, num4, num5):


    result = []
    checked = []
    try:
        
        
        if num1 == None:
            raise ValueError("Num1 is missing")
        if num2 == None:
                raise ValueError("Num2 is missing")
        if num3 == None:
            raise ValueError("Num3 is missing")
        if num4 == None:
            raise ValueError("Num4 is missing")
        if num5 == None:
            raise ValueError("Num5 is missing")
        
        else:
            input_numbers = [num1, num2, num3, num4, num5]
            all_counters = []
            return input_numbers
    except:
            return "Error with the find_counter function"
        
        # zig zag subtractions
    
def zig_zag_subtractions(input_numbers):
    try:
        subtracted_nums_array = []
        subtracted_num = input_numbers[0]
        for nums in input_numbers[1:]:
            subtracted_num = subtracted_num - nums if subtracted_num > nums else nums - subtracted_num
            subtracted_nums_array.append(subtracted_num)
            return subtracted_nums_array
    except:
        return "Problem with zig_zag_subtractions function"
    
     
    

    
all_counters = []
initial_counter = 45

# Counter function
def find_counters(winning_numbers):
    try:
        matching_counters = []
        for nums in winning_numbers:
            counter = initial_counter
            if nums <= counter:
                matching_counter = nums + counter
            else:
                matching_counter = nums - counter
            matching_counters.append(matching_counter)
            return matching_counters
    except:
        return "Problem with find_counters function"
    
    
    
# Find counters function is called
def find_matching_nums(user_input_numbers):
    try:
        match_counters = user_input_nums(user_input_numbers)
        all_counters.extend(match_counters)
        print(f"All Counters: {all_counters}")
        return all_counters
    except:
        return "Problem with find matching_nums function"
    

    
def find_processed_result(last_num, first_num): 
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
    return processed_result

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
    
        

# # Function to check for matches
# def find_match(value, list2_ab):
#     is_match = []
#     if abs(value) in list2_ab:
#         is_match.append(value)
#     return is_match


    # messages = []
    # for value in all_straight_subtracted_array:
    #     matches = find_match(value)
    #     if matches:
    #         print(f"There is a match for {value}.")
    #     else:
    #         print(f"No match found for {value}")



    
@api_view(['POST'])
def get_reponse_from_lotto_machine(request):
    if request.method == 'POST':
        # Get data from users
        try:
            num1 = request.data.get('num1')
            num2 = request.data.get('num2')
            num3 = request.data.get('num3')
            num4 = request.data.get('num4')
            num5 = request.data.get('num5')
            user_input_numbers = user_input_nums(num1, num2, num3, num4, num5)
            winning_numbers = [num1, num2, num3, num4, num5]
            get_zigz_zag_subtractions = zig_zag_subtractions(user_input_numbers)
            zig_zag_subtracted_winning_nums = []
            zig_zag_subtracted_winning_nums.extend(get_zigz_zag_subtractions)
            first_num = winning_numbers[0]
            last_num = zig_zag_subtracted_winning_nums[-1]
            all_straight_subtracted_array = straight_line_subtractions(winning_numbers)
            # ensure all numbers are positive
            # list2_ab = set(abs(value) for value in all_straight_subtracted_array)
            # is_match = find_match(value, list2_ab)
            matching_counters = find_matching_nums(user_input_numbers)
            processed_result = find_processed_result(last_num, first_num)
            return Response({'message': processed_result})
        except Exception as e:
            return Response({"message": str(e)})