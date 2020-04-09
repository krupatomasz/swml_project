import csv
import sys
import os

def convert_binary_feat(feat, first_val):
    if feat == first_val:
        return 0
    else:
        return 1

def normalise(value, floor, ceil):
    if not value:
        return 0
    value = int(value) - floor
    return value / (ceil - floor)

def main():
    csv_name = sys.argv[1]
    csv_output_name = 'converted_' + csv_name
    if not os.path.exists(csv_output_name):
        with open(csv_output_name, 'w'): pass

    with open(csv_name) as csv_file:
        with open(csv_output_name, mode='w') as csv_output_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')

            output_fieldnames = list(csv_reader.fieldnames)
            output_fieldnames.remove('Mjob')
            output_fieldnames.remove('Fjob')
            output_fieldnames.remove('reason')
            output_fieldnames.remove('guardian')
            output_fieldnames.append('Mjob_is_at_home')
            output_fieldnames.append('Mjob_is_health')
            output_fieldnames.append('Mjob_is_teacher')
            output_fieldnames.append('Mjob_is_services')
            output_fieldnames.append('Mjob_is_other')
            output_fieldnames.append('Fjob_is_at_home')
            output_fieldnames.append('Fjob_is_health')
            output_fieldnames.append('Fjob_is_teacher')
            output_fieldnames.append('Fjob_is_services')
            output_fieldnames.append('Fjob_is_other')
            output_fieldnames.append('reason_is_home')
            output_fieldnames.append('reason_is_reputation')
            output_fieldnames.append('reason_is_course')
            output_fieldnames.append('reason_is_other')
            output_fieldnames.append('guardian_is_mother')
            output_fieldnames.append('guardian_is_father')
            output_fieldnames.append('guardian_is_other')
            csv_writer = csv.DictWriter(csv_output_file, delimiter=';', fieldnames=output_fieldnames)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    csv_writer.writeheader()
                else:
                    if row['G3'] == '0':
                        continue
                    output_row = {}
                    output_row['school'] = convert_binary_feat(row['school'], 'GP')
                    output_row['sex'] = convert_binary_feat(row['sex'], 'F')
                    output_row['age'] = normalise(row['age'].strip(), 15, 22)
                    output_row['address'] = convert_binary_feat(row['address'], 'U')
                    output_row['famsize'] = convert_binary_feat(row['famsize'], 'GT3')
                    output_row['Pstatus'] = convert_binary_feat(row['Pstatus'], 'A')
                    output_row['Medu'] = normalise(row['Medu'], 0,4)
                    output_row['Fedu'] = normalise(row['Fedu'], 0,4)
                    output_row['Mjob_is_at_home'] = convert_binary_feat(row['Mjob'], 'at_home')
                    output_row['Mjob_is_health'] = convert_binary_feat(row['Mjob'], 'health')
                    output_row['Mjob_is_teacher'] = convert_binary_feat(row['Mjob'], 'teacher')
                    output_row['Mjob_is_services'] = convert_binary_feat(row['Mjob'], 'services')
                    output_row['Mjob_is_other'] = convert_binary_feat(row['Mjob'], 'other')
                    output_row['Fjob_is_at_home'] = convert_binary_feat(row['Fjob'], 'at_home')
                    output_row['Fjob_is_health'] = convert_binary_feat(row['Fjob'], 'health')
                    output_row['Fjob_is_teacher'] = convert_binary_feat(row['Fjob'], 'teacher')
                    output_row['Fjob_is_services'] = convert_binary_feat(row['Fjob'], 'services')
                    output_row['Fjob_is_other'] = convert_binary_feat(row['Fjob'], 'other')
                    output_row['reason_is_home'] = convert_binary_feat(row['reason'], 'home')
                    output_row['reason_is_reputation'] = convert_binary_feat(row['reason'], 'reputation')
                    output_row['reason_is_course'] = convert_binary_feat(row['reason'], 'course')
                    output_row['reason_is_other'] = convert_binary_feat(row['reason'], 'other')
                    output_row['guardian_is_mother'] = convert_binary_feat(row['guardian'], 'mother')
                    output_row['guardian_is_father'] = convert_binary_feat(row['guardian'], 'father')
                    output_row['guardian_is_other'] = convert_binary_feat(row['guardian'], 'other')
                    output_row['traveltime'] = normalise(row['traveltime'], 1,4)
                    output_row['studytime'] = normalise(row['studytime'], 1,4)
                    output_row['failures'] = normalise(row['failures'], 0,3)
                    output_row['schoolsup'] = convert_binary_feat(row['schoolsup'], 'no')
                    output_row['famsup'] = convert_binary_feat(row['famsup'], 'no')
                    output_row['paid'] = convert_binary_feat(row['paid'], 'no')
                    output_row['activities'] = convert_binary_feat(row['activities'], 'no')
                    output_row['nursery'] = convert_binary_feat(row['nursery'], 'no')
                    output_row['higher'] = convert_binary_feat(row['higher'], 'no')
                    output_row['internet'] = convert_binary_feat(row['internet'], 'no')
                    output_row['romantic'] = convert_binary_feat(row['romantic'], 'no')
                    output_row['famrel'] = normalise(row['famrel'], 1,5)
                    output_row['freetime'] = normalise(row['freetime'], 1,5)
                    output_row['goout'] = normalise(row['goout'], 1,5)
                    output_row['Dalc'] = normalise(row['Dalc'], 1,5)
                    output_row['Walc'] = normalise(row['Walc'], 1,5)
                    output_row['health'] = normalise(row['health'], 1,5)
                    output_row['absences'] = normalise(row['absences'], 0,93)
                    output_row['G1'] = normalise(row['G1'], 0,20)
                    output_row['G2'] = normalise(row['G2'], 0,20)
                    output_row['G3'] = normalise(row['G3'], 0,20)
                    csv_writer.writerow(output_row)
                    
                line_count += 1

if __name__ == '__main__':
    main()

