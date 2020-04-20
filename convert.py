import csv
import sys
import os

def convert_binary_feat(feat, first_val):
    if feat == first_val:
        return 1
    else:
        return 0

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
            fields_to_remove = ['Mjob', 'Fjob', 'reason', 'guardian']
            binary_feats = []
            parent_jobs = ['at_home', 'health', 'teacher', 'services', 'other']
            reasons = ['home', 'reputation', 'course', 'other']
            guardians = ['mother', 'father', 'other']
            new_Mjobs = new_Fjobs = new_reasons = new_guardians = []
            for job in parent_jobs:
                new_Mjob = 'Mjob_is_' + job
                new_Fjob = 'Fjob_is_' + job
                new_Mjobs.append(new_Mjob)
                new_Fjobs.append(new_Fjob)
                output_fieldnames.append(new_Mjob)
                output_fieldnames.append(new_Fjob)
                binary_feats.append([new_Mjob, 'Mjob', job])
                binary_feats.append([new_Fjob, 'Fjob', job])
            for reason in reasons:
                new_reason = 'reason_is_' + reason
                new_reasons.append(new_reason)
                output_fieldnames.append(new_reason)
                binary_feats.append([new_reason, 'reason', reason])
            for guardian in guardians:
                new_guardian = 'guardian_is_' + guardian
                new_guardians.append(new_guardian)
                output_fieldnames.append(new_guardian)
                binary_feats.append([new_guardian, 'guardian', guardian])
            for field in fields_to_remove:
                output_fieldnames.remove(field)

            csv_writer = csv.DictWriter(csv_output_file, delimiter=';', fieldnames=output_fieldnames)
            csv_writer.writeheader()
            for row in csv_reader:
                if row['G3'] == '0':
                    continue

                output_row = {}
                simple_binary_feats = [['school', 'GP'], ['sex', 'F'], ['address', 'U'], ['famsize', 'GT3'], ['Pstatus', 'A'], ['schoolsup', 'no'], ['famsup', 'no'], ['paid', 'no'], ['activities', 'no'], ['nursery', 'no'], ['higher', 'no'], ['internet', 'no'], ['romantic', 'no']]
                for feat in simple_binary_feats:
                    binary_feats.append([feat[0], feat[0], feat[1]])
                for feat in binary_feats:
                    output_row[feat[0]] = convert_binary_feat(row[feat[1]], feat[2])

                feats_to_normalise = [['age', 15, 22], ['Medu', 0, 4], ['Fedu', 0, 4], ['traveltime', 1, 4], ['studytime', 1, 4], ['failures', 0, 3], ['famrel', 1, 5], ['freetime', 1, 5], ['goout', 1, 5], ['Dalc', 1, 5], ['Walc', 1, 5], ['health', 1, 5], ['absences', 0, 93], ['G1', 0, 20], ['G2', 0, 20], ['G3', 0, 20]]
                for feat in feats_to_normalise:
                    output_row[feat[0]] = normalise(row[feat[0]], feat[1], feat[2])

                csv_writer.writerow(output_row)

if __name__ == '__main__':
    main()

