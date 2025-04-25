import streamlit as st
import ipaddress

def to_binary(address):
    octets = address.split('.')
    binary_octets = []
    for octet in octets:
        binary_octet = bin(int(octet))[2:].zfill(8)
        binary_octets.append(binary_octet)
    return '.'.join(binary_octets)

def calculate_subnet(ip_str, subnet_str):
    try:
        interface = ipaddress.IPv4Interface(f"{ip_str}/{subnet_str}")
        network = interface.network
        
        # Network details
        results = {
            "network_address": str(network.network_address),
            "broadcast_address": str(network.broadcast_address),
            "subnet_mask": str(interface.netmask),
            "cidr": network.prefixlen,
            "total_hosts": network.num_addresses,
            "usable_hosts": max(0, network.num_addresses - 2),
            "ip_binary": to_binary(str(interface.ip)),
            "subnet_binary": to_binary(str(interface.netmask))
        }
        
        # Host range calculation
        if results["usable_hosts"] > 0:
            first_host = network.network_address + 1
            last_host = network.broadcast_address - 1
            results["host_range"] = f"{first_host} - {last_host}"
        else:
            results["host_range"] = "No usable hosts"
            
        return results
    
    except ValueError as e:
        st.error(f"Invalid IP or subnet mask: {e}")
        return None

# Streamlit UI
st.title("IP Subnet Calculator")
st.subheader("Student Information")
st.write("Name: hatem")
st.write("Student ID: xxxxxxx")
st.write("Group: xx")

with st.form("subnet_form"):
    col1, col2 = st.columns(2)
    with col1:
        ip_address = st.text_input("IP Address", placeholder="e.g., 192.168.1.1")
    with col2:
        subnet_mask = st.text_input("Subnet Mask", placeholder="e.g., 255.255.255.0 or 24")
    
    calculate_btn = st.form_submit_button("Calculate")
    clear_btn = st.form_submit_button("Clear")

if clear_btn:
    st.experimental_rerun()

if calculate_btn:
    if not ip_address or not subnet_mask:
        st.warning("Please enter both IP address and subnet mask.")
    else:
        results = calculate_subnet(ip_address, subnet_mask)
        if results:
            st.subheader("Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Network Address:** {results['network_address']}")
                st.markdown(f"**Broadcast Address:** {results['broadcast_address']}")
                st.markdown(f"**Subnet Mask:** {results['subnet_mask']}")
                st.markdown(f"**CIDR Notation:** /{results['cidr']}")
            
            with col2:
                st.markdown(f"**Total Hosts:** {results['total_hosts']}")
                st.markdown(f"**Usable Hosts:** {results['usable_hosts']}")
                st.markdown(f"**Host Range:** {results['host_range']}")
            
            st.markdown("---")
            st.markdown(f"**IP Address (Binary):** {results['ip_binary']}")
            st.markdown(f"**Subnet Mask (Binary):** {results['subnet_binary']}")