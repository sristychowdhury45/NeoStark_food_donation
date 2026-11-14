
import json
import os


class FoodDonationSystem:

    def __init__(self):
        self.donation_file = "donations.json"
        self.user_file = "users.json"

        self.donations = self.load_data(self.donation_file)
        self.users = self.load_data(self.user_file)

    # Load JSON records
    def load_data(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    # Save JSON records
    def save_data(self):
        with open(self.donation_file, "w") as file:
            json.dump(self.donations, file, indent=4)

        with open(self.user_file, "w") as file:
            json.dump(self.users, file, indent=4)

    # Create a food donation
    def create_donation(self):
        print("\nCreate Donation")

        food = input("Food Name: ").strip()
        quantity = input("Quantity: ").strip()
        location = input("Location: ").strip()
        available_until = input("Available Until: ").strip()
        contact = input("Contact Information: ").strip()

        if not all([food, quantity, location,
                    available_until, contact]):
            print("Error: All fields are required.")
            return

        donation_id = f"DON{len(self.donations) + 1:03d}"

        donation = {
            "donation_id": donation_id,
            "food": food,
            "quantity": quantity,
            "location": location,
            "available_until": available_until,
            "contact": contact,
            "status": "Available",
            "volunteer": None
        }

        self.donations.append(donation)

        self.users.append({
            "role": "Donor",
            "contact": contact
        })

        self.save_data()

        print("\nDonation Created Successfully.")
        print("Donation ID:", donation_id)
        print("Status: Available")

    # View available donations
    def view_donations(self):
        print("\nAvailable Donations")
        print("-------------------")

        available = [
            d for d in self.donations
            if d["status"] == "Available"
        ]

        if not available:
            print("No available donations.")
            return

        for d in available:
            print("\n", d["donation_id"])
            print("Food:", d["food"])
            print("Quantity:", d["quantity"])
            print("Location:", d["location"])
            print("Status:", d["status"])

    # Volunteer accepts a donation
    def claim_donation(self):
        donation_id = input("\nEnter Donation ID: ").strip()
        volunteer_id = input("Enter Volunteer ID: ").strip()

        if not donation_id or not volunteer_id:
            print("Error: Both IDs are required.")
            return

        donation = next(
            (d for d in self.donations
             if d["donation_id"] == donation_id),
            None
        )

        if donation is None:
            print("Error: Donation not found.")
            return

        if donation["status"] != "Available":
            print("Error: Donation is not available.")
            return

        donation["status"] = "Claimed"
        donation["volunteer"] = volunteer_id

        if not any(
            u.get("volunteer_id") == volunteer_id
            for u in self.users
        ):
            self.users.append({
                "role": "Volunteer",
                "volunteer_id": volunteer_id
            })

        self.save_data()

        print("\nDonation", donation_id)
        print("Status:", donation["status"])
        print("Volunteer:", volunteer_id)

    # Update donation status
    def update_status(self, donation_id, current_status, new_status):
        donation = next(
            (d for d in self.donations
             if d["donation_id"] == donation_id),
            None
        )

        if donation is None:
            print("Error: Donation not found.")
            return

        if donation["status"] != current_status:
            print("Error: Invalid status transition.")
            return

        donation["status"] = new_status
        self.save_data()

        print("Donation", donation_id)
        print("Status:", new_status)

    # Main menu
    def run(self):
        while True:
            print("\nFood Donation Management System")
            print("1. Create Donation")
            print("2. View Available Donations")
            print("3. Claim Donation")
            print("4. Mark as Picked Up")
            print("5. Mark as Delivered")
            print("6. Exit")

            choice = input("\nChoose an option: ").strip()

            try:
                if choice == "1":
                    self.create_donation()

                elif choice == "2":
                    self.view_donations()

                elif choice == "3":
                    self.claim_donation()

                elif choice == "4":
                    donation_id = input("Enter Donation ID: ").strip()
                    self.update_status(
                        donation_id, "Claimed", "Picked Up"
                    )

                elif choice == "5":
                    donation_id = input("Enter Donation ID: ").strip()
                    self.update_status(
                        donation_id, "Picked Up", "Delivered"
                    )

                elif choice == "6":
                    print("Exiting Food Donation Management System.")
                    break

                else:
                    print("Invalid choice. Please try again.")

            except (ValueError, OSError) as e:
                print("Error:", e)


# Run the application
if __name__ == "__main__":
    system = FoodDonationSystem()
    system.run()
